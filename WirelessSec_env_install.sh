#Wireless Security and OSWP Exam Environment Setup

#!/bin/bash
# Display system information
echo "Gathering system information..."
echo "Operating System Details:"
cat /etc/os-release
echo
echo "Kernel Details:"
uname -a
echo
# Update system and install mandatory tools
echo "Updating system and installing mandatory tools..."
sudo apt update && sudo apt install -y \
    aircrack-ng \
    hashcat \
    reaver \
    bully \
    macchanger \
    hostapd \
    hostapd-mana \
    dnsmasq \
    python3 \
    python3-pip \
    libssl-dev \
    freeradius \
    mdk4 \
    apache2 \
    libapache2-mod-php \
    php \
    screen \
    isc-dhcp-server
# Install optional recommended tools
echo "Installing optional recommended tools..."
sudo apt install -y pixiewps hcxdumptool hcxtools
sudo apt install -y wireshark tshark
sudo apt install -y sslstrip ettercap-graphical bettercap
# Clone and set up GitHub tools
echo "Cloning and setting up eaphammer..."
git clone https://github.com/s0lst1c3/eaphammer.git && cd eaphammer && sudo ./kali-setup && cd ..
echo "Cloning airgeddon..."
git clone https://github.com/v1s1t0r1sh3r3/airgeddon.git
echo "Cloning and setting up wifiphisher..."
git clone https://github.com/wifiphisher/wifiphisher.git && cd wifiphisher && sudo python3 setup.py install && cd ..
# Verification step
echo "Verifying installed tools..."
tools=("aircrack-ng" "hashcat" "reaver" "bully" "macchanger" "pixiewps" "hcxdumptool" "hcxtools" "wireshark" "tshark" "sslstrip" "ettercap" "bettercap")
for tool in "${tools[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "$tool is installed successfully."
    else
        echo "Error: $tool is not installed."
    fi
done
echo "Installation completed!"
