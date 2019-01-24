import queue


accounts_list = queue.Queue()
accounts_done = 0

success_key = 'Logged in as'
fail_key = 'Invalid username or password!'


def load_accounts():
    with open('accounts.txt','r') as accounts_file:
        for line in accounts_file:
            accounts_list.put(line.strip())


def parse_accounts(accounts_list):
        uname = accounts_list.split(':')[0]
        password = accounts_list.split(':')[1]
        login_details = {'uname': uname, 'password': password}
        return login_details


def is_logged_in(response, login_details):
    global accounts_done
    accounts_done += 1

    html = response.text
    if fail_key in html:
        print('[-] N' + str(accounts_done) + '[-] Failed - ' + str(login_details['uname']) + ':' + str(login_details['password']))
        return False
    elif success_key in html:
        print('[+] N' + str(accounts_done) + '[+] Success - ' + str(login_details['uname']) + ':' + str(login_details['password']))
        save_success(login_details)
        return True


def save_success(login_details):
        out = open('success.txt','a')
        out.write(str(login_details['uname']) + ':' + str(login_details['password']))
        out.write("\n")
        out.close()


def put_account(login_details):
    accounts_list.put(login_details['uname'] + ':' + login_details['password'])


def is_account_empty(accounts_list):
    return accounts_list.qsize() <= 0
