import requests
import json
import sys
import time


def create_cloudflare_zone(auth_email, auth_key, domain):
    # Set up the API request headers
    headers = {
        "X-Auth-Email": auth_email,
        "X-Auth-Key": auth_key,
        "Content-Type": "application/json"
    }

    # Set up the API request body
    data = {
        "name": domain,
        "jump_start": False
    }

    # Make the API request to create the zone
    response = requests.post(
        "https://api.cloudflare.com/client/v4/zones",
        headers=headers,
        json=data
    )

    # Check the response status code to see if the request was successful
    if response.status_code == 200:
        # save zone id to a file
        with open('zone_id.txt', 'w') as f:
            f.write(response.json()['result']['id'])
        print("Zone created successfully!")
        return response.json()['result']['id']
    else:
        print(f"Error creating zone: {response.json()}")
        return None


def set_ssl_full(auth_email, auth_key, zone_id):
    # Set up the API request headers
    headers = {
        "X-Auth-Email": auth_email,
        "X-Auth-Key": auth_key,
        "Content-Type": "application/json"
    }

    # Set up the API request body
    data = {
        "value": "full"
    }

    # Make the API request to set SSL to full
    response = requests.patch(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl",
        headers=headers,
        json=data
    )

    # Check the response status code to see if the request was successful
    if response.status_code == 200:
        print("SSL set to full successfully!")
    else:
        print(f"Error setting SSL to full: {response.json()}")


def enable_ws_proxy(auth_email, auth_key, zone_id):
    # Set up the API request headers
    headers = {
        "X-Auth-Email": auth_email,
        "X-Auth-Key": auth_key,
        "Content-Type": "application/json"
    }

    # Set up the API request body
    data = {
        "value": "on"
    }

    # Make the API request to enable ws proxy
    response = requests.patch(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/websockets",
        headers=headers,
        json=data
    )

    # Check the response status code to see if the request was successful
    if response.status_code == 200:
        print("Websocket proxy enabled successfully!")
    else:
        print(f"Error enabling websocket proxy: {response.json()}")


def cloudflare_dns_record_create(auth_email, auth_key, zone_id, record):

    # Set up the API request headers
    headers = {
        "X-Auth-Email": auth_email,
        "X-Auth-Key": auth_key,
        "Content-Type": "application/json"
    }

    # Make the API request to create the DNS record
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
        headers=headers,
        json=record
    )

    # Check the response status code to see if the request was successful
    if response.status_code == 200:
        print("DNS record created successfully!")
    else:
        print(f"Error creating DNS record: {response.json()}")


if __name__ == "__main__":
    auth_email = sys.argv[1]
    auth_key = sys.argv[2]
    domain = sys.argv[3]
    server_ip = sys.argv[4]

    # Create a zone
    zone_id = create_cloudflare_zone(auth_email, auth_key, domain)
    if zone_id is None:
        print("Error creating zone")
        sys.exit(1)
    conf = {
        "auth_email": auth_email,
        "auth_key": auth_key,
        "zone_id": zone_id,
        "domain": domain
    }
    with open('cloudflare.conf', 'w') as f:
        json.dump(conf, f, indent=4)
    # set ssl to full
    set_ssl_full(auth_email, auth_key, zone_id)
    enable_ws_proxy(auth_email, auth_key, zone_id)
    # The DNS record to create
    time.sleep(90)
    record = {
        "type": "A",
        "name": "@",
        "content": server_ip,
        "proxied": True
    }
    cloudflare_dns_record_create(
        auth_email=auth_email, auth_key=auth_key, zone_id=zone_id, record=record)
