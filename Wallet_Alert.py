

###Python Script to automaticly alert Wallet changes###

import time
import hashlib
from urllib.request import urlopen, Request
from plyer import notification
import pandas as pd


def checkWallet(wallet):

    url = Request(f"https://www.blockchain.com/btc/address/{wallet}")
    response = urlopen(url).read()

    currentHash = hashlib.sha224(response).hexdigest()
    print("running")
    time.sleep(10)
    while True:
        try:
            # perform the get request and store it in a var
            response = urlopen(url).read()
            print(response)

            # create a hash
            currentHash = hashlib.sha224(response).hexdigest()

            # wait for 30 seconds
            time.sleep(30)

            # perform the get request
            response = urlopen(url).read()

            # create a new hash
            newHash = hashlib.sha224(response).hexdigest()

            # check if new hash is same as the previous hash
            if newHash == currentHash:
                continue

            # if something changed in the hashes
            else:
                # notify
                print("something changed")

                # again read the website
                response = urlopen(url).read()

                # create a hash
                currentHash = hashlib.sha224(response).hexdigest()

                # wait for 30 seconds
                time.sleep(30)
                continue

        # To handle exceptions
        except Exception as e:
            print("error")

checkWallet("32ANbidud9ABk7AGPnRvbcKwJ6CQqJm6HE")




#
# if __name__ == '__main__':
#     wallet_list = []
#     df = pd.read_excel(r"C:\Users\GZL_010\Desktop\wallets.xlsx")
#
#     for col in df.columns:
#         wallet_list.append(col)
#         for val in df[col]:
#             wallet_list.append(val)
#     print(wallet_list)
#
#     for wallet in wallet_list:
#         try:
#             checkWallet(wallet)
#         except Exception as Error:
#             print(f"Error happened on {wallet}")
#             try:
#                 print("Retrying - in 5 seconds")
#                 time.sleep(5)
#                 checkWallet(wallet)
#             except Exception as Error:
#                 print("Retry Failed " + str(Error))
#
#             print("Couldn't complete due to " + str(Error))
