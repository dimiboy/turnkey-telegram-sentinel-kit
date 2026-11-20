#!/usr/bin/env python3
"""
Telegram Sentinel Daemon - Autonomous Server Health & Alert System
Turnkey monitoring agent with smart deduplication, rate limiting, and Telegram delivery.
"""

import os
import sys
import time
import socket
import logging
from datetime import datetime
import psutil
import requests
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("sentinel")

# Load environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
SERVER_NAME = os.getenv("SERVER_NAME", socket.gethostname())
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD_PERCENT", "85"))
RAM_THRESHOLD = float(os.getenv("RAM_THRESHOLD_PERCENT", "90"))
DISK_THRESHOLD = float(os.getenv("DISK_THRESHOLD_PERCENT", "90"))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))
COOLDOWN_MINUTES = int(os.getenv("ALERT_COOLDOWN_MINUTES", "15"))

last_alerts = {}

def send_telegram(text: str, parse_mode: str = "HTML") -> bool:
    if not BOT_TOKEN or not ADMIN_CHAT_ID or "your_bot_token" in BOT_TOKEN:
        logger.warning("Telegram credentials not configured. Skipping send.")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False

def can_alert(alert_key: str) -> bool:
    now = time.time()
    last_time = last_alerts.get(alert_key, 0)
    if now - last_time > (COOLDOWN_MINUTES * 60):
        last_alerts[alert_key] = now
        return True
    return False

def check_system():
    # CPU
    cpu = psutil.cpu_percent(interval=1)
    if cpu >= CPU_THRESHOLD and can_alert("cpu"):
        msg = f"⚠️ <b>High CPU Alert</b> on <code>{SERVER_NAME}</code>\nUsage: <b>{cpu}%</b> (Threshold: {CPU_THRESHOLD}%)"
        logger.warning(msg)
        send_telegram(msg)

    # Memory
    ram = psutil.virtual_memory()
    if ram.percent >= RAM_THRESHOLD and can_alert("ram"):
        msg = (f"⚠️ <b>High RAM Alert</b> on <code>{SERVER_NAME}</code>\n"
               f"Usage: <b>{ram.percent}%</b> ({round(ram.used / (1024**3), 1)}GB / {round(ram.total / (1024**3), 1)}GB)")
        logger.warning(msg)
        send_telegram(msg)

    # Disks
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            if usage.percent >= DISK_THRESHOLD and can_alert(f"disk_{part.mountpoint}"):
                msg = (f"🚨 <b>Disk Space Critical</b> on <code>{SERVER_NAME}</code>\n"
                       f"Mount: <code>{part.mountpoint}</code>\n"
                       f"Usage: <b>{usage.percent}%</b> (Free: {round(usage.free / (1024**3), 1)}GB)")
                logger.error(msg)
                send_telegram(msg)
        except PermissionError:
            continue

def main():
    logger.info(f"Starting Telegram Sentinel for {SERVER_NAME}...")
    boot_msg = (f"🛡️ <b>Sentinel Daemon Online</b>\n"
                f"Server: <code>{SERVER_NAME}</code>\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Monitoring CPU ({CPU_THRESHOLD}%), RAM ({RAM_THRESHOLD}%), Disks ({DISK_THRESHOLD}%)")
    send_telegram(boot_msg)

    while True:
        try:
            check_system()
        except Exception as e:
            logger.error(f"Error in sentinel cycle: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
