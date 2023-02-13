#!/bin/bash

read -p "Enter the domain name: " domain
read -p "Enter the Cloudflare email: " auth_email
read -p "Enter the Cloudflare Global key: " auth_key
# get server external IP
ip=$(curl -s https://api.ipify.org)



# sleep 10 seconds to wait for DNS propagation
# animation: https://stackoverflow.com/a/1249834/104380
echo -ne '###                       (10%)\r'
sleep 10
sudo apt update
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
echo -ne '#########                 (30%)\r'
python3 cloudflare.py $auth_email $auth_key $domain $ip
echo -ne '#############             (35%)\r'
sudo apt install certbot nginx -y
echo -ne '################          (45%)\r'
sudo systemctl stop nginx
sudo certbot certonly --standalone --non-interactive --agree-tos --email your-email@$domain -d $domain
echo -ne '####################      (60%)\r'
echo "Certificate generated for $domain"
echo -ne '#######################   (80%)\r'
mkdir /etc/v2ray/
sudo ln -s /etc/letsencrypt/live/$domain/ /etc/letsencrypt/default
sudo ln -s /etc/letsencrypt/live/$domain/fullchain.pem /etc/v2ray/fullchain.pem
sudo ln -s /etc/letsencrypt/live/$domain/privkey.pem /etc/v2ray/privkey.pem
cp nginx.conf /etc/nginx/sites-available/default
sudo systemctl restart nginx
python3 xray.py $domain
echo -ne '########################  (90%)\r' 
cp config.json /usr/local/etc/xray/config.json
sudo systemctl restart xray
echo -ne '######################### (100%)\r'