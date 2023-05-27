from json import loads

import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware


class ChainData:
    def __init__(self, url):
        self.url = url
        self.web3 = Web3(Web3.HTTPProvider(url))
        # self.web2 = Web3(Web3.HTTPProvider("https://gnfd-testnet-sp-1.nodereal.io"))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.WEI = 1000000000000000000

    def get_block(self, height='latest'):
        if height == 'latest':
            height = self.get_block_num()
        r = requests.get(self.url + f"block_results?height={height}")
        res = {
            'height': height
        }
        # print(height)
        src = loads(r.text)['result']['txs_results']
        count_of_transactions = (len(src if src else []))
        res = {
            'height': height,
            "count_of_transactions": count_of_transactions
        }
        if count_of_transactions:

            # print(height)
            # print(r.text)
            # src = loads(r.text)['result']['txs_results'][0]
            for i in range(count_of_transactions):
                # print(i, loads(src[i]['log'])[0]['events'][-2]['attributes'])

                res['transactions'] = res.get('transactions', []) + [
                    {
                        'address': loads(src[i]['log'])[0]['events'][0]['attributes'][1]['value'],
                        'type': loads(src[i]['log'])[0]['events'][0]['attributes'][0]['value'].split('.')[-1],
                        'time': loads(src[i]['log'])[0]['events'][-2]['attributes'][2]['value']
                    }
                ]
            # return res
        return res

    def get_block_num(self):
        return self.web3.eth.get_block_number()

    def get_last_trans(self, limit=10):
        num = self.get_block_num()
        # print(block)
        # num = block['number']
        data = []
        for i in range(limit):
            block = self.get_block(num - i)
            if block['count_of_transactions'] > 0:
               for tx in block['transactions']:
                    tx['height'] = num - i
               data += block['transactions']

        return data

    def get_balance(self, wallet_address):
        checksum_address = Web3.to_checksum_address(wallet_address)
        balance = self.web3.eth.get_balance(checksum_address)
        return balance / self.WEI

    # def accounts(self):
    #     r = requests.get(self.url + "genesis")
    #
    #     return r.text

    # def data(self, hash_data):
    #     return self.web3.h

    def providers(self):
        pass

    def accounts(self):
        pass

    def get_user_trans_count(self, wallet_address):
        wallet_address = Web3.to_checksum_address(wallet_address)
        balance = self.get_balance(wallet_address)
        block = self.get_block_num()

        n = self.web3.eth.get_transaction_count(wallet_address, block)
        return n
        # return self.web3.eth.get_transaction_count(Web3.to_checksum_address(wallet_address))

    # def convert_to_bnb(self, num):
    #     return num / 10000000000


# ch = ChainData(url="https://data-seed-prebsc-1-s1.binance.org:8545")
ch = ChainData(url='https://gnfd-testnet-fullnode-tendermint-us.bnbchain.org/')
data = ch.get_last_trans()
print(data)
print(ch.get_balance("0xb73c0aac4c1e606c6e495d848196355e6cb30381"))
wallet = "0xc9c16bff2a82282818fae17e9722a3ad1e702eb7"
# print((loads(ch.accounts())['result']['genesis']['app_state']['auth']['accounts']))
