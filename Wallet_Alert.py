import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from plyer import notification


def check_wallet():
    # target URL
    print("Please Enter Wallet Address:")
    wallet = input()
    url = f"https://www.blockchain.com/btc/address/{wallet}"

    # act like a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(HTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

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
                    print("\n+-+-+-+-+- Start Monitoring -+-+-+-+-+ \n" + url + " - " + str(datetime.now()))
                    print("\nOriginal Transaction amount is    " + str(transaction_amount) + "    - " + str(datetime
                                                                                                            .now()))
                else:
                    print("\n" + "+-+-+-+-+-" + "Changes detected at: " + str(datetime.now()) + "+-+-+-+-+-")
                    old_page = prev_version
                    print("+-+-+-+ OLD-PAGE IS : " + str(old_page) + " - " + str(datetime.now()))
                    new_page = (soup.split()[transaction_amount_index])
                    print("+-+-+-+ NEW-PAGE IS : " + str(new_page) + " - " + str(datetime.now()))

                    # Pop Up Notification
                    try:
                        notification.notify(
                            title=f"{wallet} has new transaction",
                            message=f"{url}" + "\n" + str(datetime.now()),
                            app_icon=r"C:\dev\Wallet-Alert\bell-icon.png",
                            timeout=120,
                            ticker=True,
                            toast=False
                        )
                    except Exception as error:
                        print("Notification Error: " + str(error))

                    print("Script ShutDown")
                    break
            else:
                print("No Changes " + str(datetime.now()))
            time.sleep(60)
            continue
        except Exception as error:
            print("Main Script Error - " + str(error) + " \n-----------Script Closing-----------")
            break


check_wallet()
