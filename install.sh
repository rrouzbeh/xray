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
sudo apt-get update > /dev/null
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install > /dev/null
echo -ne '#########                 (30%)\r'
python3 cloudflare.py $auth_email $auth_key $domain $ip
echo -ne '#############             (35%)\r'
sudo apt-get install certbot python3-certbot-dns-cloudflare -y > /dev/null
mkdir /root/.secrets/
touch /root/.secrets/cloudflare.ini
echo "dns_cloudflare_email = $auth_email" >> /root/.secrets/cloudflare.ini
echo "dns_cloudflare_api_key" = $auth_key >> /root/.secrets/cloudflare.ini
sudo chmod 0700 /root/.secrets/
sudo chmod 0400 /root/.secrets/cloudflare.ini
echo -ne '################          (45%)\r'
sudo certbot certonly --dns-cloudflare --dns-cloudflare-credentials /root/.secrets/cloudflare.ini  --non-interactive --agree-tos --email your-email@$domain -d $domain,*.$domain --preferred-challenges dns-0
echo -ne '####################      (60%)\r'
echo "Certificate generated for $domain"
echo -ne '#######################   (80%)\r'
install -d -o nobody -g nogroup /etc/v2ray/
install -m 644 -o nobody -g nogroup /etc/letsencrypt/live/$domain/fullchain.pem -t /etc/v2ray/
install -m 600 -o nobody -g nogroup /etc/letsencrypt/live/$domain/privkey.pem -t /etc/v2ray/
python3 xray.py $domain
echo -ne '########################  (90%)\r' 
cp config.json /usr/local/etc/xray/config.json
sudo systemctl restart xray
echo -ne '######################### (100%)\r'