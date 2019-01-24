import queue
import requests


proxy_list = queue.Queue()

def load_proxylist():
    with open('proxylist.txt','r') as proxy_file:
        for line in proxy_file:
            proxy_list.put('https://' + line.strip())

# Parsed for requests payload ( instead of using queue.get() )

def get_proxy(proxy_list):
    return {'https': proxy_list.get()}


def is_proxy_good(proxy_ip):
    r = requests.get('https://www.google.com/',proxies=proxy_ip,timeout=10)
    if str(200) in r:
        return True
    return False


def put_proxy(proxy_ip):
    proxy_list.put(proxy_ip['https'])


def is_proxy_empy(proxy_list):
    return proxy_list <= 0
