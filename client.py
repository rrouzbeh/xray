import base64
import sys
import random
import string
import requests
import json


def generate_random_domain(subdomains, top_domains):
    subdomain = random.choice(subdomains)
    top_domain = random.choice(top_domains)
    domain = subdomain + "-" + top_domain
    random_string = ''.join(random.choices(
        string.ascii_lowercase, k=6))
    return domain + random_string

# file lines to list


def file_to_list(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines


def gen_vless_qr_code(server_config):
    # Generate vless:// link
    vless_link = f"vless://{server_config['user_id']}@{server_config['address']}:{server_config['port']}?type=ws&security=tls&path=%2F&host={server_config['tls_server_name']}&sni={server_config['tls_server_name']}#{server_config['tls_server_name']}"
    # Generate QR code
    qr_code = base64.b64encode(vless_link.encode('utf-8')).decode('utf-8')
    return qr_code, vless_link


def cloudflare_dns_record_create(auth_email, auth_key, zone_id, record, server_ip):
    print("Creating DNS record...")
    print(f"DNS record: {record}")
    print(f"Zone ID: {zone_id}")
    # Set up the API request headers
    headers = {
        "X-Auth-Email": auth_email,
        "X-Auth-Key": auth_key,
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": record,
        "content": server_ip,
        "proxied": True
    }
    # Make the API request to create the DNS record
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
        headers=headers,
        json=data
    )

    # Check the response status code to see if the request was successful
    if response.status_code == 200:
        print("DNS record created successfully!")
    else:
        print(f"Error creating DNS record: {response.json()}")


if __name__ == '__main__':
    subdomains = ["www", "blog", "ftp", "mail", "webmail", "remote", "ns1", "ns2", "ns3", "ns4", "ns5", "ns6", "ns7", "ns8", "ns9", "test", "dev", "stage",
                  "beta", "alpha", "docs", "docs-google", "drive", "drive-google", "calendar", "calendar-google", "maps", "maps-google", "app", "app-google", "apps"]
    top_domains = ["digikala", "alibaba", "soroush", "snapp", "divar", "zomato", "cafebazaar", "cheetah", "myket", "aparat", "sibapp", "parsijoo", "irna", "irib", "mehrnews", "varzesh3", "tnews",
                   "iran-daily", "iran-emrooz", "iran-front", "iran-varzeshi", "iran-newspaper", "iran-review", "iran-student", "iran-times", "iran-tribune", "iran-press", "iran-dailynews", "iran-news"]

    with open('cloudflare.conf', 'r') as f:
        conf = json.load(f)
    cf_ips = file_to_list('cf_ips.txt')
    # sort cf_ips by second column and add it to a new list
    cf_ips = sorted(cf_ips, key=lambda x: int(x.strip().split(",")[1]))
    # get server external IP
    ip = requests.get('https://api.ipify.org').text
    with open('uuid.txt', 'r') as f:
        user_id = f.read()
    for i in range(5):
        address = cf_ips[i].strip().split(",")[0]
        record = generate_random_domain(subdomains, top_domains)
        domain = f'{record}.{conf["domain"]}'
        server_config = {
            "address": address,
            "port": 443,
            "user_id": user_id,
            "alter_id": 64,
            "tls_server_name": domain,
            "ws_path": "/"
        }
        if i < 4:
            cloudflare_dns_record_create(
                conf['auth_email'], conf['auth_key'], conf['zone_id'], record, ip)
        else:
            server_config["address"] = ip
        qr_code, vless_link = gen_vless_qr_code(server_config)
        print(qr_code)
        print(vless_link)
