import brute
import proxies
import accounts
from brute import Worker


def main():

    proxies.load_proxylist() # puts the proxies in a queue inside proxy_list variable
    accounts.load_accounts() # puts the accounts in queue file

    print('* Number of proxies loaded : ' + str(proxies.proxy_list.qsize()))
    print('* Number of accounts loaded : ' + str(accounts.accounts_list.qsize()))
    print('Starting ....')

    brute.run_loop()

    print('Done')


if __name__ == "__main__":
    main()
