# Turnkey 1-Click Telegram Server Sentinel & Alert Stack

A complete, production-ready server health monitoring and instant Telegram alerting suite for HomeLab servers, VPS instances, Raspberry Pi, and local PCs.

---

## ⚡ 5-Minute Quick Start

### Option A: Run via Docker (Recommended)
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` with your Bot Token and Telegram Chat ID:
   ```bash
   nano .env
   ```
3. Start the stack:
   ```bash
   docker compose up -d
   ```
4. Access Uptime Kuma monitoring dashboard at: `http://localhost:3001`

---

### Option B: Run Directly via Python
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your `.env` file.
3. Run the sentinel:
   ```bash
   python sentinel_daemon.py
   ```

---

### Option C: Run as a Linux Systemd Service
1. Copy the directory to `/opt/telegram-sentinel`
2. Install the service file:
   ```bash
   sudo cp systemd/telegram-sentinel.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now telegram-sentinel
   ```

---

## 🛡️ Features Included
- **Instant Boot Notification**: Alerts your Telegram the moment the machine boots or container spins up.
- **CPU & RAM Sentry**: Traps spikes above configurable thresholds.
- **Disk Partition Watch**: Warns before storage exhaustion causes database crashes.
- **Smart Anti-Spam Rate Limiting**: Cooldown ensures you get alerted once, not spammed 100 times a minute.
- **Zero-Cloud Dependency**: Runs entirely locally on your host or Docker.
