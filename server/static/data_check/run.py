import schedule
import time
import csv
from server.static.data_check.main import ChainData
# 1685198725
ch = ChainData(url='https://gnfd-testnet-fullnode-tendermint-us.bnbchain.org/')


def acc_num():
    with open('accounts_num.csv', 'a', newline='') as csvfile:
        fieldnames = ['account_num', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        acc_num, timestamp = (ch.get_accounts_num(), int(time.time()))
        writer.writerow({'account_num': acc_num, 'time': timestamp})


def seal_providers():
    with open('seal_providers.csv', 'a', newline='') as csvfile:
        fieldnames = ['provider', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        last_trans, timestamp = (ch.get_last_trans("MsgSealObject", limit=500), int(time.time()))
        nums = {}
        for i in range(len(last_trans)):
            if not nums.get("STATUS", False):
              nums[last_trans[i]['provider']] = nums.get(last_trans[i]['provider'], 0) + 1

            # print(nums)
        for pr, count in nums.items():
                writer.writerow({'provider': pr, 'count': count})


# def bucket_providers():
#     with open('bucket_providers.csv', 'a', newline='') as csvfile:
#         fieldnames = ['provider', 'count']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         last_trans = ch.get_last_trans("MsgCreateBucket", limit=300)
#         nums = {}
#         for i in range(len(last_trans)):
#             if not nums.get("STATUS", False):
#               nums[last_trans[i]['provider']] = nums.get(last_trans[i]['provider'], 0) + 1
#
#         # print(nums)
#         for pr, count in nums.items():
#             writer.writerow({'provider': pr, 'count': count})


def clean_file():
    with open('seal_providers.csv', 'w', newline='') as csvfile:
        pass
    with open('bucket_providers.csv', 'w', newline='') as csvfile:
        pass
        # fieldnames = ['provider', 'count']
        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        # last_trans = ch.get_last_trans("MsgCreateBucket", limit=300)
        # nums = {}
        # for i in range(len(last_trans)):
        #     if not nums.get("STATUS", False):
        #       nums[last_trans[i]['provider']] = nums.get(last_trans[i]['provider'], 0) + 1
        #
        # # print(nums)
        # for pr, count in nums.items():
        #     writer.writerow({'provider': pr, 'count': count})


# seal_providers()
# schedule.every(1).minutes.do(acc_num)
# schedule.every(3).hours.do(acc_num)
schedule.every().day.at("10:25").do(clean_file)
schedule.every().day.at("10:30").do(seal_providers)
# schedule.every().day.at("10:35").do(bucket_providers)
# # # schedule.every(5).to(10).minutes.do(job)
# # # schedule.every().monday.do(job)
# # # schedule.every().wednesday.at("13:15").do(job)
# # # schedule.every().minute.at(":17").do(job)
# # # нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
# while True:
#     schedule.run_pending()
#     time.sleep(1)