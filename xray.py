import uuid
import json
import sys


def open_example_config(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


def gen_config(config, uuid, domain):
    cert_path = f'/etc/letsencrypt/live/{domain}/'
    config = open_example_config('config_example.json')
    config['inbounds'][0]['settings']['clients'][0]['id'] = uuid
    config['inbounds'][0]['streamSettings']['tlsSettings']['certificates'][0]['certificateFile'] = cert_path + 'fullchain.pem'
    config['inbounds'][0]['streamSettings']['tlsSettings']['certificates'][0]['keyFile'] = cert_path + 'privkey.pem'
    config['inbounds'][0]['streamSettings']['tlsSettings']['serverName'] = domain
    return config


if __name__ == '__main__':
    config = open_example_config('config_example.json')
    uuid = str(uuid.uuid4())
    domain = sys.argv[1]
    res = gen_config(config, uuid, domain)
    # create config.json
    with open('config.json', 'w') as f:
        json.dump(res, f, indent=4)
    # create uuid.txt
    with open('uuid.txt', 'w') as f:
        f.write(uuid)
    print('config.json created successfully!')
