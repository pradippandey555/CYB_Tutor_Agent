# apis/shodan_api.py - Query Shodan for host info
import os, shodan
from dotenv import load_dotenv

load_dotenv()

api = shodan.Shodan(os.getenv("SHODAN_API_KEY"))

def host_lookup(ip):
    try:
        host = api.host(ip)
        print(f"IP: {host['ip_str']}")
        print(f"Org: {host.get('org', 'N/A')}")
        print(f"Country: {host.get('country_name', 'N/A')}")
        for item in host['data']:
            print(f"Port {item['port']}: {item.get('transport', 'tcp').upper()}")
            print(f"Banner: {item.get('data', '')[:100]}")
    except shodan.APIError as e:
        print(f"Shodan error: {e}")

if __name__ == "__main__":
    ip = input("Enter IP to look up: ")
    host_lookup(ip)