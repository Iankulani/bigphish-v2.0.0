#!/bin/bash
# install.sh - BIG-PHISH Installation Script for Alpine Linux
# Author: Ian Carter Kulani
# Version: 2.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="bigphish"
APP_DIR="/opt/bigphish"
DATA_DIR="/var/lib/bigphish"
LOG_DIR="/var/log/bigphish"
CONFIG_DIR="/etc/bigphish"
SERVICE_USER="bigphish"
SERVICE_GROUP="bigphish"

print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root!"
        exit 1
    fi
}

detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VER=$VERSION_ID
        print_success "Detected OS: $OS $VER"
    else
        print_error "Cannot detect OS"
        exit 1
    fi
}

install_alpine_deps() {
    print_status "Installing Alpine Linux dependencies..."
    
    apk update
    apk add --no-cache \
        python3 \
        py3-pip \
        python3-dev \
        build-base \
        linux-headers \
        libpcap-dev \
        nmap \
        nmap-scripts \
        curl \
        bind-tools \
        traceroute \
        openssh-client \
        whois \
        git \
        iptables \
        tcpdump \
        net-tools \
        nikto \
        sudo \
        shadow \
        supervisor \
        nginx \
        apache2-utils \
        openssl \
        ca-certificates
    
    print_success "Alpine dependencies installed"
}

install_ubuntu_deps() {
    print_status "Installing Ubuntu/Debian dependencies..."
    
    apt-get update
    apt-get install -y \
        python3 \
        python3-pip \
        python3-dev \
        build-essential \
        libpcap-dev \
        nmap \
        curl \
        dnsutils \
        traceroute \
        openssh-client \
        whois \
        git \
        iptables \
        tcpdump \
        net-tools \
        nikto \
        sudo \
        nginx \
        apache2-utils \
        openssl \
        ca-certificates \
        supervisor
    
    print_success "Ubuntu dependencies installed"
}

install_python_deps() {
    print_status "Installing Python dependencies..."
    
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
    print_success "Python dependencies installed"
}

create_user_and_dirs() {
    print_status "Creating user and directories..."
    
    # Create group if not exists
    if ! getent group $SERVICE_GROUP >/dev/null; then
        groupadd -r $SERVICE_GROUP
    fi
    
    # Create user if not exists
    if ! id $SERVICE_USER >/dev/null 2>&1; then
        useradd -r -g $SERVICE_GROUP -s /sbin/nologin -d $APP_DIR $SERVICE_USER
    fi
    
    # Create directories
    mkdir -p $APP_DIR $DATA_DIR $LOG_DIR $CONFIG_DIR
    
    # Create subdirectories
    mkdir -p $DATA_DIR/payloads
    mkdir -p $DATA_DIR/workspaces
    mkdir -p $DATA_DIR/scans
    mkdir -p $DATA_DIR/nikto_results
    mkdir -p $DATA_DIR/whatsapp_session
    mkdir -p $DATA_DIR/phishing_pages
    mkdir -p $DATA_DIR/traffic_logs
    mkdir -p $DATA_DIR/phishing_templates
    mkdir -p $DATA_DIR/captured_credentials
    mkdir -p $DATA_DIR/ssh_keys
    mkdir -p $DATA_DIR/ssh_logs
    mkdir -p $DATA_DIR/time_history
    mkdir -p $DATA_DIR/wordlists
    
    # Set permissions
    chown -R $SERVICE_USER:$SERVICE_GROUP $APP_DIR $DATA_DIR $LOG_DIR $CONFIG_DIR
    chmod -R 755 $APP_DIR $DATA_DIR $LOG_DIR $CONFIG_DIR
    
    print_success "User and directories created"
}

copy_files() {
    print_status "Copying application files..."
    
    # Copy main application
    cp bigphish.py $APP_DIR/
    cp requirements.txt $APP_DIR/
    
    # Set executable
    chmod +x $APP_DIR/bigphish.py
    chown $SERVICE_USER:$SERVICE_GROUP $APP_DIR/bigphish.py
    
    print_success "Files copied to $APP_DIR"
}

create_config() {
    print_status "Creating configuration..."
    
    cat > $CONFIG_DIR/config.json << EOF
{
    "monitoring": {"enabled": true, "port_scan_threshold": 10},
    "scanning": {"default_ports": "1-1000", "timeout": 30},
    "security": {"auto_block": false, "log_level": "INFO"},
    "nikto": {"enabled": true, "timeout": 300},
    "traffic_generation": {"enabled": true, "max_duration": 300, "allow_floods": false},
    "social_engineering": {"enabled": true, "default_port": 8080, "capture_credentials": true},
    "crunch": {"enabled": true, "max_file_size_mb": 1024, "default_output_dir": "$DATA_DIR/wordlists"},
    "ssh": {"enabled": true, "default_timeout": 30, "max_connections": 5}
}
EOF
    
    chown $SERVICE_USER:$SERVICE_GROUP $CONFIG_DIR/config.json
    chmod 600 $CONFIG_DIR/config.json
    
    print_success "Configuration created at $CONFIG_DIR/config.json"
}

create_systemd_service() {
    print_status "Creating systemd service..."
    
    cat > /etc/systemd/system/bigphish.service << EOF
[Unit]
Description=BIG-PHISH Cybersecurity Command Center
Documentation=https://github.com/bigphish/bigphish
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_GROUP
WorkingDirectory=$APP_DIR
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/bin/python3 $APP_DIR/bigphish.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=bigphish

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$DATA_DIR $LOG_DIR $CONFIG_DIR

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable bigphish.service
    
    print_success "Systemd service created"
}

create_openrc_service() {
    print_status "Creating OpenRC service for Alpine..."
    
    cat > /etc/init.d/bigphish << EOF
#!/sbin/openrc-run

name="bigphish"
description="BIG-PHISH Cybersecurity Command Center"
command="/usr/bin/python3"
command_args="$APP_DIR/bigphish.py"
command_user="$SERVICE_USER"
pidfile="/run/\$RC_SVCNAME.pid"
command_background=true

depend() {
    need net
    after firewall
}

start_pre() {
    checkpath -f -d -o $SERVICE_USER:$SERVICE_GROUP $DATA_DIR
    checkpath -f -d -o $SERVICE_USER:$SERVICE_GROUP $LOG_DIR
    checkpath -f -d -o $SERVICE_USER:$SERVICE_GROUP $CONFIG_DIR
}

stop() {
    ebegin "Stopping $name"
    start-stop-daemon --stop --quiet --pidfile \$pidfile
    eend \$?
}
EOF
    
    chmod +x /etc/init.d/bigphish
    rc-update add bigphish default
    
    print_success "OpenRC service created"
}

create_nginx_config() {
    print_status "Creating Nginx configuration..."
    
    cat > /etc/nginx/conf.d/bigphish.conf << EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /api {
        proxy_pass http://127.0.0.1:8080/api;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF
    
    # Test and reload nginx
    nginx -t && rc-service nginx restart || systemctl restart nginx
    
    print_success "Nginx configuration created"
}

setup_firewall() {
    print_status "Setting up firewall rules..."
    
    # Allow SSH
    if command -v iptables >/dev/null; then
        iptables -A INPUT -p tcp --dport 22 -j ACCEPT
        iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
        iptables -A INPUT -p tcp --dport 80 -j ACCEPT
        iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
        
        # Save rules
        if [ -f /etc/alpine-release ]; then
            rc-service iptables save
        else
            iptables-save > /etc/iptables/rules.v4
        fi
    fi
    
    print_success "Firewall rules configured"
}

create_logrotate() {
    print_status "Creating logrotate configuration..."
    
    cat > /etc/logrotate.d/bigphish << EOF
$LOG_DIR/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 $SERVICE_USER $SERVICE_GROUP
    sharedscripts
    postrotate
        systemctl kill -s USR1 bigphish.service || true
    endscript
}
EOF
    
    print_success "Logrotate configured"
}

setup_monitoring() {
    print_status "Setting up monitoring..."
    
    # Create health check script
    cat > /usr/local/bin/bigphish-health.sh << 'EOF'
#!/bin/bash
if curl -f http://localhost:8080/ > /dev/null 2>&1; then
    echo "BIG-PHISH is healthy"
    exit 0
else
    echo "BIG-PHISH is unhealthy"
    exit 1
fi
EOF
    
    chmod +x /usr/local/bin/bigphish-health.sh
    
    # Add to crontab for monitoring
    echo "*/5 * * * * /usr/local/bin/bigphish-health.sh >> /var/log/bigphish/health.log 2>&1" | crontab -
    
    print_success "Monitoring configured"
}

display_summary() {
    echo ""
    echo "=========================================="
    echo -e "${GREEN}BIG-PHISH Installation Complete!${NC}"
    echo "=========================================="
    echo ""
    echo -e "${BLUE}Installation Details:${NC}"
    echo "  Application Directory: $APP_DIR"
    echo "  Data Directory: $DATA_DIR"
    echo "  Log Directory: $LOG_DIR"
    echo "  Config Directory: $CONFIG_DIR"
    echo "  Service User: $SERVICE_USER"
    echo ""
    echo -e "${BLUE}Access Information:${NC}"
    echo "  Web Interface: http://localhost:8080"
    echo "  API Endpoint: http://localhost:8080/api"
    echo ""
    echo -e "${BLUE}Management Commands:${NC}"
    
    if [ -f /etc/alpine-release ]; then
        echo "  Start: rc-service bigphish start"
        echo "  Stop: rc-service bigphish stop"
        echo "  Restart: rc-service bigphish restart"
        echo "  Status: rc-service bigphish status"
    else
        echo "  Start: systemctl start bigphish"
        echo "  Stop: systemctl stop bigphish"
        echo "  Restart: systemctl restart bigphish"
        echo "  Status: systemctl status bigphish"
    fi
    
    echo ""
    echo -e "${BLUE}Logs:${NC}"
    echo "  Journal: journalctl -u bigphish -f"
    echo "  Log Files: $LOG_DIR/bigphish.log"
    echo ""
    echo -e "${YELLOW}⚠️  Important Notes:${NC}"
    echo "  1. Run with sudo/root for full functionality"
    echo "  2. Configure platform bots in the web interface"
    echo "  3. Check firewall rules if accessing remotely"
    echo "  4. Default credentials are configured in $CONFIG_DIR/config.json"
    echo ""
    echo -e "${GREEN}Thank you for installing BIG-PHISH!${NC}"
}

main() {
    print_status "Starting BIG-PHISH installation..."
    
    check_root
    detect_os
    
    # Install dependencies based on OS
    if [ "$OS" = "alpine" ]; then
        install_alpine_deps
    elif [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        install_ubuntu_deps
    else
        print_error "Unsupported OS: $OS"
        exit 1
    fi
    
    install_python_deps
    create_user_and_dirs
    copy_files
    create_config
    
    # Create service based on init system
    if [ -f /etc/alpine-release ]; then
        create_openrc_service
    else
        create_systemd_service
    fi
    
    create_nginx_config
    setup_firewall
    create_logrotate
    setup_monitoring
    
    display_summary
    
    # Ask to start service
    read -p "Start BIG-PHISH now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -f /etc/alpine-release ]; then
            rc-service bigphish start
            rc-service nginx restart
        else
            systemctl start bigphish
            systemctl restart nginx
        fi
        print_success "BIG-PHISH started!"
    fi
}

main "$@"