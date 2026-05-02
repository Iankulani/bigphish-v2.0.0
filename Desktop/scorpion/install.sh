#!/bin/bash
# Scorpion-Effect Installation Script for Linux/Mac

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   🦂 SCORPION-EFFECT INSTALLER v2.0${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check Python version
check_python() {
    if command -v python3 &>/dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if (( $(echo "$PYTHON_VERSION >= 3.7" | bc -l) )); then
            echo -e "${GREEN}[✓] Python $PYTHON_VERSION found${NC}"
            return 0
        fi
    fi
    echo -e "${RED}[✗] Python 3.7+ required${NC}"
    exit 1
}

# Check OS and install system dependencies
install_system_deps() {
    echo -e "${BLUE}[1/6] Installing system dependencies...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &>/dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-venv nmap traceroute whois dnsutils net-tools iputils-ping
        elif command -v yum &>/dev/null; then
            sudo yum install -y python3-pip nmap traceroute whois bind-utils net-tools
        elif command -v apk &>/dev/null; then
            sudo apk add python3 py3-pip nmap traceroute whois bind-tools net-tools
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &>/dev/null; then
            brew install python3 nmap
        else
            echo -e "${YELLOW}[!] Homebrew not found. Install manually: https://brew.sh${NC}"
        fi
    fi
}

# Create virtual environment
setup_venv() {
    echo -e "${BLUE}[2/6] Creating virtual environment...${NC}"
    python3 -m venv scorpion_venv
    source scorpion_venv/bin/activate
}

# Install Python packages
install_python_packages() {
    echo -e "${BLUE}[3/6] Installing Python packages...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
}

# Create directories
create_directories() {
    echo -e "${BLUE}[4/6] Creating directories...${NC}"
    mkdir -p .scorpion-effect reports phishing_data logs
}

# Create configuration
create_config() {
    echo -e "${BLUE}[5/6] Creating configuration...${NC}"
    if [ ! -f .scorpion-effect/config.json ]; then
        cat > .scorpion-effect/config.json << EOF
{
    "web_port": 5000,
    "enable_web": true,
    "enable_discord": false,
    "enable_telegram": false,
    "enable_slack": false,
    "enable_google_chat": false
}
EOF
    fi
}

# Create startup script
create_startup_script() {
    echo -e "${BLUE}[6/6] Creating startup script...${NC}"
    cat > start_scorpion.sh << 'EOF'
#!/bin/bash
source scorpion_venv/bin/activate
python3 scorpion_effect.py
EOF
    chmod +x start_scorpion.sh
}

# Main installation
main() {
    check_python
    install_system_deps
    setup_venv
    install_python_packages
    create_directories
    create_config
    create_startup_script
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}   ✅ INSTALLATION COMPLETE!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}To run Scorpion-Effect:${NC}"
    echo -e "  ${BLUE}./start_scorpion.sh${NC}"
    echo ""
    echo -e "${YELLOW}Or manually:${NC}"
    echo -e "  ${BLUE}source scorpion_venv/bin/activate${NC}"
    echo -e "  ${BLUE}python3 scorpion_effect.py${NC}"
    echo ""
    echo -e "${YELLOW}Web interface:${NC} ${BLUE}http://localhost:5000${NC}"
    echo ""
}

# Run installation
main "$@"