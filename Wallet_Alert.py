import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime
from plyer import notification


def check_wallet():
    # target URL
    print("Please Enter Wallet Adress:")
    wallet = input()
    url = f"https://www.blockchain.com/btc/address/{wallet}"

    # act like a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    prev_version = ""
    first_run = True
    while True:

        # download the page
        response = requests.get(url, headers=headers)
        # parse the downloaded homepage
        soup = BeautifulSoup(response.text, "lxml")

        # remove all scripts and styles and get transaction number
        for script in soup(["script", "style"]):
            script.extract()
        soup = soup.get_text()
        transaction_amount_index = (soup.split().index("transacted") + 1)
        transaction_amount = (soup.split()[transaction_amount_index])

        # compare the page text to the previous version
        try:
            if prev_version != transaction_amount:
                # on the first run - just memorize the page
                if first_run:
                    prev_version = transaction_amount
                    first_run = False
                    print("+-+-+-+-+- Start Monitoring -+-+-+-+-+ \n" + url + " - " + str(datetime.now()))
                    print("\nTransaction amount is " + str(transaction_amount) + "  - " + str(datetime.now()))
                else:
                    print("Changes detected at: " + str(datetime.now()))
                    old_page = prev_version
                    print("+-+-+-+-+-+-OLDPAGE IS : " + str(old_page) + " - " + str(datetime.now()))
                    new_page = (soup.split()[transaction_amount_index])
                    print("+-+-+-+-+-+-NEWPAGE IS : " + str(new_page) + " - " + str(datetime.now()))

                    # compare versions and highlight changes using difflib
                    # d = difflib.Differ()
                    # diff = d.compare(old_page, new_page)

                    diff = difflib.context_diff(old_page, new_page, n=20)
                    print('\n'.join(diff))

                    # Pop Up Notification
                    notification.notify(
                        title=f"{wallet} has new transaction",
                        message=f"{url}" + "/n" + str(datetime.now()),
                        app_icon="bell-icon.png",
                        timeout=120
                    )
                    print("Script ShutDown")
                    break
            else:
                print("No Changes " + str(datetime.now()))
            time.sleep(60)
            continue
        except Exception as error:
            print("Error - " + str(error))


check_wallet()
