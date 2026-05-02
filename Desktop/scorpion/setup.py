#!/usr/bin/env python3
"""Setup script for Scorpion-Effect package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scorpion-effect",
    version="2.0.0",
    author="Security Research Team",
    description="Multi-Platform Cybersecurity Command & Control Center",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/security/scorpion-effect",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "psutil>=5.9.0",
        "paramiko>=3.0.0",
        "Flask>=2.3.0",
        "Flask-SocketIO>=5.3.0",
        "discord.py>=2.3.0",
        "telethon>=1.34.0",
        "slack-sdk>=3.25.0",
        "qrcode[pil]>=7.4.0",
        "whois>=0.9.27",
        "python-nmap>=0.7.1",
    ],
    entry_points={
        "console_scripts": [
            "scorpion=scorpion_effect:main",
        ],
    },
)