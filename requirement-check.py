#!/usr/bin/env python3
"""
Dependency Checker for Big-Phish Framework
Checks all required packages and system tools
"""

import sys
import subprocess
import importlib
import shutil
import platform
from typing import Dict, List, Tuple

class RequirementChecker:
    """Check and verify all dependencies for Big-Phish"""
    
    def __init__(self):
        self.results = {
            'python_version': None,
            'system_tools': [],
            'python_packages': [],
            'optional_packages': [],
            'errors': []
        }
    
    def check_python_version(self) -> bool:
        """Check Python version requirement"""
        version = sys.version_info
        required = (3, 7)
        
        if version >= required:
            self.results['python_version'] = f"✓ Python {version.major}.{version.minor}.{version.micro}"
            return True
        else:
            self.results['python_version'] = f"✗ Python {version.major}.{version.minor} (requires 3.7+)"
            return False
    
    def check_system_tool(self, tool_name: str) -> bool:
        """Check if a system tool is available"""
        path = shutil.which(tool_name)
        if path:
            self.results['system_tools'].append(f"✓ {tool_name} ({path})")
            return True
        else:
            self.results['system_tools'].append(f"✗ {tool_name} (not found)")
            return False
    
    def check_python_package(self, package_name: str, import_name: str = None) -> bool:
        """Check if a Python package is installed"""
        import_name = import_name or package_name.replace('-', '_')
        try:
            importlib.import_module(import_name)
            self.results['python_packages'].append(f"✓ {package_name}")
            return True
        except ImportError:
            self.results['python_packages'].append(f"✗ {package_name} (not installed)")
            return False
    
    def check_optional_package(self, package_name: str, import_name: str = None) -> bool:
        """Check optional package (warning only)"""
        import_name = import_name or package_name.replace('-', '_')
        try:
            importlib.import_module(import_name)
            self.results['optional_packages'].append(f"✓ {package_name}")
            return True
        except ImportError:
            self.results['optional_packages'].append(f"⚠ {package_name} (optional)")
            return False
    
    def get_install_command(self) -> str:
        """Get the pip install command for missing packages"""
        missing = []
        for item in self.results['python_packages']:
            if item.startswith('✗'):
                pkg = item.split(' ')[1]
                missing.append(pkg)
        
        for item in self.results['optional_packages']:
            if item.startswith('⚠'):
                pkg = item.split(' ')[1]
                if pkg not in missing:
                    missing.append(pkg)
        
        if missing:
            return f"pip install {' '.join(missing)}"
        return ""
    
    def run_all_checks(self):
        """Run all dependency checks"""
        print("🔍 Big-Phish Dependency Checker\n" + "="*50)
        
        # Python version
        print("\n📌 Python Version:")
        self.check_python_version()
        print(f"  {self.results['python_version']}")
        
        # System tools
        print("\n🔧 System Tools:")
        tools = ['ping', 'nmap', 'curl', 'dig', 'traceroute', 'ssh', 'nikto']
        for tool in tools:
            self.check_system_tool(tool)
        
        for result in self.results['system_tools']:
            print(f"  {result}")
        
        # Core packages
        print("\n📦 Core Python Packages:")
        core_packages = [
            ('cryptography', 'cryptography'),
            ('paramiko', 'paramiko'),
            ('scapy', 'scapy'),
            ('requests', 'requests'),
            ('psutil', 'psutil'),
            ('colorama', 'colorama'),
            ('whois', 'whois'),
            ('qrcode', 'qrcode'),
            ('pyshorteners', 'pyshorteners'),
        ]
        
        for pkg, imp in core_packages:
            self.check_python_package(pkg, imp)
        
        for result in self.results['python_packages']:
            print(f"  {result}")
        
        # Optional packages
        print("\n🎮 Optional Packages (for platform bots):")
        optional_packages = [
            ('discord.py', 'discord'),
            ('telethon', 'telethon'),
            ('slack-sdk', 'slack_sdk'),
            ('selenium', 'selenium'),
            ('webdriver-manager', 'webdriver_manager'),
            ('google-api-python-client', 'googleapiclient'),
            ('flask', 'flask'),
            ('flask-socketio', 'flask_socketio'),
        ]
        
        for pkg, imp in optional_packages:
            self.check_optional_package(pkg, imp)
        
        for result in self.results['optional_packages']:
            print(f"  {result}")
        
        # Summary
        print("\n" + "="*50)
        print("📊 SUMMARY")
        print("="*50)
        
        python_ok = '✓' in self.results['python_version']
        core_ok = all('✓' in r for r in self.results['python_packages'])
        tools_ok = any('✓' in r for r in self.results['system_tools'])
        
        print(f"Python Version: {'✓ OK' if python_ok else '✗ FAIL'}")
        print(f"Core Packages: {'✓ OK' if core_ok else '✗ FAIL'}")
        print(f"System Tools: {'✓ OK (some found)' if tools_ok else '⚠ Limited'}")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS")
        print("-"*50)
        
        install_cmd = self.get_install_command()
        if install_cmd:
            print(f"Install missing packages: {install_cmd}")
        
        # Platform-specific instructions
        system = platform.system().lower()
        
        if system == 'linux':
            print("\nFor Linux, install missing system tools:")
            print("  sudo apt-get update")
            print("  sudo apt-get install -y nmap traceroute nikto")
        elif system == 'darwin':
            print("\nFor macOS, install missing tools with Homebrew:")
            print("  brew install nmap nikto")
        elif system == 'windows':
            print("\nFor Windows, download tools manually:")
            print("  - Nmap: https://nmap.org/download.html")
            print("  - Nikto: Requires Perl installation")
        
        # Check for admin/root
        if system == 'linux' and shutil.which('sudo'):
            print("\n⚠ Some features require root/sudo (traffic generation, firewall rules)")
        
        return core_ok and python_ok
    
    def print_banner(self):
        """Print colorful banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║     🐋 BIG-PHISH DEPENDENCY CHECKER - Verify Requirements     ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

def main():
    """Main entry point"""
    checker = RequirementChecker()
    checker.print_banner()
    success = checker.run_all_checks()
    
    print("\n" + "="*50)
    if success:
        print("✅ All core dependencies satisfied!")
        print("   You can run Big-Phish with: python3 big_phish.py")
    else:
        print("❌ Missing core dependencies")
        print("   Please install missing packages and try again")
    
    print("="*50)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())