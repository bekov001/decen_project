import sys
import time
from json import loads
from random import randint

import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware


PROVIDERS = {
    '0xb573f5c174f33af0ca033c8a287061c1538fb130': "Titan",
    "0xa3ac8c0999b73f028122ce609e318c7da09cb752": "Nodereal",
    "0x3cfc8b2095da8f0722412dc16f8a067942d2c697": "Gadgetron",
    "0xe42b5ad90aff1e8ad90f76e02541a71ca9d41a11": "Neuronet",
    "0x5e340c0721bd5f49627e7e34eb94bedfa575e993": "Thorax",
    "0xc6fa3f3640e3b594335efab349abdd4a82c83736": "Voltbot",
    "0x7715d0680fe84ca6d7eaef6e8a7cace29a4c0064": "Cogsworth",
    "0x22804504786f44289d4156e7317142e25b92c00e": "Zenon"


}

DATA = {
  "nodereal": "https://gnfd-testnet-sp-1.nodereal.io",
  "titan": "https://gnfd-testnet-sp-7.bnbchain.org",
  "gadgetron": "https://gnfd-testnet-sp-6.bnbchain.org",
  "voltbot": "https://gnfd-testnet-sp-5.bnbchain.org",
  "cogsworth": "https://gnfd-testnet-sp-1.bnbchain.org",
  "neuronet": "https://gnfd-testnet-sp-3.bnbchain.org",
  "thorax": "https://gnfd-testnet-sp-4.bnbchain.org",
  "zenon": "https://gnfd-testnet-sp-4.bnbchain.org"
}

SEAL_PROVIDERS = {
    "0xE4F1Ac4B9312724D2819347c5c91252b650C4AEb": "Zenon",
    "0x43416fd2dd08bc6f2004b9a5fa53686b7f541d58": "Gadgetron",
    "0x47b07b9dba6117f800b4f7d2e31b0c4b32127a90": "Neuronet",
    "0xfce3084e2ac67e1f698926b7fbcbd2204bfa7f92": "Thorax",
    "0x3f92219ef03f8af218f9da601eaf254db022f13d": "Voltbot",
    "0x735851c190f6999826f2a128dd53b9ca02f32c25": "Cogsworth",
    "0x674d969927aba4ee9cd05e5079655bb099d83d85": "Titan"

}


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
        # print(r.text)
        src = loads(r.text)['result']['txs_results']
        count_of_transactions = (len(src if src else []))
        res = {
            'height': height,
            "count_of_transactions": count_of_transactions
        }
        if count_of_transactions:

            # print(r.text)
            # src = loads(r.text)['result']['txs_results'][6]
            # print(src)
            for i in range(count_of_transactions):
                # print(i, PROVIDERS.get(loads(src[i]['log'])[0]['events'][0]['attributes'][1]['value']))
                if 'failed to execute message' not in src[i]['log']:
                    # print(src[i + 1]['log'], 'failed to execute message' in src[i + 1]['log'])
                    # print(loads(src[i]['log'])[0]['events'][0]['attributes'][0]['value'].split('.')[-1],)
                    res['transactions'] = res.get('transactions', []) + [
                        {
                            'address': loads(src[i]['log'])[0]['events'][0]['attributes'][1]['value'],
                            'type': loads(src[i]['log'])[0]['events'][0]['attributes'][0]['value'].split('.')[-1],

                        }
                    ]
                    if res['transactions'][-1]['type'] != "MsgClaim":
                        res['transactions'][-1]['time'] = loads(src[i]['log'])[0]['events'][-2]['attributes'][2]['value']
                    else:
                        pass
                        # print(loads(src[i]['log']))
                        # res['transactions'][-1]['time'] = \
                        # loads(src[i]['log'])[0]['events'][-5]['attributes'][2]['value']
                    if res['transactions'][-1]['type'] == 'MsgSealObject':
                        res['transactions'][-1]['provider'] = SEAL_PROVIDERS.get(loads(src[i]['log'])[0]['events'][0]['attributes'][1]['value'])
                    elif res['transactions'][-1]['type'] == 'MsgCreateBucket':
                        res['transactions'][-1]['provider'] = PROVIDERS.get(loads(src[i]['log'])[0]['events'][1]['attributes'][6]['value'][1:-1].lower())
                        res['transactions'][-1]['time'] = loads(src[i]['log'])[0]['events'][1]['attributes'][3]['value']
                        # res['transactions'][-1]['provider'] = PROVIDERS.get(
                        #     loads(src[i]['log'])[0]['events'][0]['attributes'][1][
                        #         'value'])
                else:
                    res['transactions'] = res.get('transactions', []) + [{'STATUS': "FAILED"}]
            # return res
        return res

    def get_block_num(self):
        return self.web3.eth.get_block_number()

    def get_price(self, provider, timestamp):
        providers = {v: k for k, v in PROVIDERS.items()}
        r = requests.get(self.url + f"greenfield/sp/get_sp_storage_price_by_time/{providers.get(provider.capitalize())}/{timestamp}")
        # print(r.text)
        return float(loads(r.text)["sp_storage_price"]["store_price"])

    def get_last_trans(self, type_msg, limit=20, provider='all'):
        num = self.get_block_num()
        # print(block)
        # num = block['number']
        data = []
        if provider == 'all':
            for i in range(limit):
                block = self.get_block(num - i)

                if block['count_of_transactions'] > 0:
                    for tx in block['transactions']:
                        if tx['type'] == type_msg:
                            tx['height'] = num - i
                            data += [tx]
        else:
            i = 0
            n = 0
            while n < limit:
                block = self.get_block(num - i)
                # print(block)
                if block['count_of_transactions'] > 0:
                    for tx in block['transactions']:
                        # print(tx, tx['provider'])
                        if tx.get('provider', False) == provider:
                            tx['height'] = num - i
                            data += [tx]
                            n += 1
                i += 1
        return data

    def get_balance(self, wallet_address):
        checksum_address = Web3.to_checksum_address(wallet_address)
        balance = self.web3.eth.get_balance(checksum_address)
        return balance / self.WEI

    def get_accounts_num(self):
        r = requests.get(f"{self.url}cosmos/auth/v1beta1/accounts")
        return loads(r.text)['pagination']['total']

    def providers(self):
        pass

    def get_uptime(self):
        book = {}
        for address, name in PROVIDERS.items():
            book[name] = randint(970, 1000) / 10
        return book

    def get_sc(self):
        book = {}
        for address, name in PROVIDERS.items():
            book[name] = str((self.get_balance(address) / self.get_price(name, int(time.time()))) / pow(10, 2))
        return book

    def get_providers_status(self):
        r = requests.get(f"{self.url}greenfield/storage_providers")
        res = loads(r.text)['sps']
        data = {}
        for i in res:
            status = i['status']
            name = i['description']['moniker']
            data[name] = status

        return data

    def get_latency(self):
        book = {}
        for name in DATA.keys():
            # name = 'gadgetron'
            URL = DATA[name]
            start = time.time()
            res = requests.get(URL + f"/view/{name}/home.css")
            book[name] = ((time.time() - start))
        return book


    def get_bandwidth(self):
        book = {}
        for name in DATA.keys():
            # name = 'gadgetron'
            URL = DATA[name]
            start = time.time()
            res = requests.get(URL + f"/view/{name}/home.css")
            book[name] = sys.getsizeof(res.text) / (time.time() - start)
            # print("WORK" if "Invalid" not in res.text else "FAIL")
        return book


if "__main__" == __name__:
    # ch = ChainData(url="https://data-seed-prebsc-1-s1.binance.org:8545")
    ch = ChainData(url='https://gnfd-testnet-fullnode-tendermint-us.bnbchain.org/')
    print(ch.get_providers_status())
# wallet = "0xc9c16bff2a82282818fae17e9722a3ad1e702eb7"
# print((loads(ch.accounts())['result']['genesis']['app_state']['auth']['accounts']))
