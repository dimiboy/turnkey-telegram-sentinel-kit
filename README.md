# 1-Click Production Telegram Server Sentinel & Uptime Stack

[![Ko-fi Shop](https://img.shields.io/badge/Ko--fi-Get%20Kit%20($4.99)-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/s/d516f950ec)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

A turnkey, production-ready server watchdog and uptime monitoring stack. Delivers instant Telegram alerts on server reboot, high CPU load, RAM saturation, low disk space, and crash events in under 3 minutes.

> **🛒 Download the complete production kit on [Ko-fi Shop](https://ko-fi.com/s/d516f950ec)** (or Pay-What-You-Want).

---

## 📦 What's Inside the Kit

- **`docker-compose.yml`**: Pre-configured multi-container stack combining the Sentinel watchdog daemon and Uptime Kuma monitoring UI.
- **`sentinel_daemon.py`**: Production-hardened Python background monitor (<20MB RAM consumption).
- **Smart Anti-Spam Rate Limiter**: 15-minute deduplication window to prevent alert storms during transient spikes.
- **Linux `systemd` templates**: Ready for Ubuntu, Debian, Raspberry Pi OS, and Arch.
- **Windows Silent Runner**: VBS / PowerShell launcher for headless Windows execution.
- **`QUICKSTART.md`**: 5-minute setup checklist.

---

## ⚡ Quick Start (Docker)

1. Clone or extract the kit:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` with your Telegram Bot Token & Chat ID:
   ```env
   TELEGRAM_BOT_TOKEN=your_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   CPU_THRESHOLD=85
   RAM_THRESHOLD=90
   DISK_THRESHOLD=90
   ```
3. Launch:
   ```bash
   docker compose up -d
   ```

You will immediately receive a **"🟢 Server Sentinel Online"** message in Telegram.

---

## ☕ Support & Author

Developed by [DimusTech](https://youtube.com/c/dimustech) / [Dima K.](https://ko-fi.com/dimiboy)
- Shop: [ko-fi.com/dimiboy/shop](https://ko-fi.com/dimiboy/shop)
- Web Tools: [rtl-cleaner.pages.dev](https://rtl-cleaner.pages.dev) | [thumbsplit.dimustech.net](https://thumbsplit.dimustech.net)
