# Xray vless-tls-ws Setup Script

## Prerequisites

- A registered domain name and access to its DNS records
- A Cloudflare account and API key
- A server running Ubuntu or a derivative
- curl and python3 installed on the server

## Cloudflare Global API Key

1. Log in to your Cloudflare account.
2. Click on the profile icon on the top right corner and select "My profile".
3. Click on the "API Tokens" tab.
4. Under the "Global API Key" section, click on the "View" button.

## Usage

```
git clone https://github.com/rrouzbeh/xray
cd xray
chmod +x install.sh
./install.sh
python client.py
```

## Note

This script assumes that curl and python3 are installed on your server. If not, install them with `sudo apt-get install curl python3`.
