import os
from json import dumps

import requests
import sys
import time

# from pysecp256k1 import *
from sha3 import keccak_256
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1

DATA = {
  "nodereal": "https://gnfd-testnet-sp-1.nodereal.io",
  "titan": "https://gnfd-testnet-sp-7.bnbchain.org",
  "gadgetron": "https://gnfd-testnet-sp-6.bnbchain.org",
  "voltbot": "https://gnfd-testnet-sp-5.bnbchain.org",
  "cogsworth": "https://gnfd-testnet-sp-1.bnbchain.org"
}


def sign():
    creator = "0x789683B40332A10aD0e2791465C7A00048081404"
    bucket_name = "gadgetron"
    objectName = "myobject"
    payloadSize = 2048
    visibility = "VISIBILITY_TYPE_PRIVATE"
    contentType = "image/jpeg"
    expiredHeight = 0
    # sig = nil
    expectChecksums = ["/v6ljJzIDPXduF53SkOdi8bt7GK73pVTDwq4N8qwbo8=",
                       "BCp9ZKWB7y7pg/IQWIAcw1ZjtwXmxV9i+o4PGOzHCYk=",
                       "TJ/iTQh4vyxmW8Ovpcr8ake9L0zm6GrTObhOKhgG+vY=",
                       "QW7N9tm0i+ZajFEHIwSRbkUyq7BltN/WNCvGdzNec+Q=",
                       "GKjb5A/cXxNx7L/c9P+xjfBXfZ1J6rffla3mdVy3Piw=",
                       "oc09LXqM8jZcIEqFyxrFBD6qO5yNGGRvLntN01U753g=",
                       "R4/dCYCqjlIdjmvaou1lGCIL245jsmlWWAG2qREa01M="]
    expectSecondarySpAddresses = ["0xf040BaaD4966842dAF83a536048a25Cf8eFF9ea0",
                                  "0xC117E319CE0C54C1C5F0e3E59B6647c5a5F0c3a8",
                                  "0x6dE810250b34059657e2C820D675232a9D884659",
                                  "0xca807A58caF20B6a4E3eDa3531788179E5bc816b",
                                  "0x20Bb76D063a6d2B18B6DaBb2aC985234a4B9eDe0",
                                  "0xa35eD99A0b4D26Bf7F74DC9D81FbfAB6A7f103Df"]

    # Users should convert json string to byte array. Then convert byte array to get lowercase hexadecimal string result and the result will be put into X-Gnfd-Unsigned-Msg header.
    src = {
      "bucket_name": bucket_name,
      "content_type": "image/jpeg",
      "creator": creator,
      "object_name": "myobject",
      "payload_size": "2048",
      "redundancy_type": "REDUNDANCY_EC_TYPE",
      "visibility": "VISIBILITY_TYPE_PRIVATE"
    }
    # src = bytearray.fromhex((dumps(src)))
    b = bytearray(map(ord, dumps(src)))
    p = ''.join('{:02x}'.format(x) for x in b)
    # b(map(ord, src))
    return p


def get_request(url, method="GET"):
    http_method = method
    CanonicalUri = url
    CanonicalQueryString = ""
    canonical_headers = dumps({

    })
    signed_headers = ""
    return "\n".join([http_method, CanonicalUri, CanonicalQueryString, canonical_headers, signed_headers]
                     )


def auth(url):
    auth_type = "authTypeV1"
    canonical_request = get_request(url)
    string_to_sign = keccak_256(sha256(canonical_request.encode("utf-8")).hexdigest().encode()).hexdigest().encode()
    # val = int.from_bytes(string_to_sign.digest(), 'big')
    # string_to_sign = ('%064x' % val)

    signature = str(((sk.sign(string_to_sign)).hex()))
    print(signature)
    authorization = auth_type + " ECDSA-secp256k1 " + str(string_to_sign.decode()) + ":" + signature
    print(authorization)
    return authorization


sk = SigningKey.generate(curve=SECP256k1)  # uses NIST192p
vk = sk.verifying_key
# print(a)
URL = DATA['nodereal']
au = auth(URL + "/greenfield/admin/v1/get-approval")

private_key = sha256(b"seckey").hexdigest()
a = sign()

payload = {
  'Authentication': au,
  'X-Gnfd-Unsigned-Msg': a
}
print(payload)
res = requests.get(URL + "/greenfield/admin/v1/get-approval", headers=payload, params={"action":"CreateObject"})
print(res.text)
# def downloadFile(url, directory) :
#     localFilename = url.split('/')[-1]
#     with open(directory + '/' + localFilename, 'wb') as f:
#       start = time.time()
#       r = requests.get(url, stream=True)
#       total_length = r.headers.get('content-length')
#       dl = 0
#       if total_length is None: # no content length header
#         f.write(r.content)
#       else:
#         for chunk in r.iter_content(1024):
#           dl += len(chunk)
#           f.write(chunk)
#           done = int(50 * dl / total_length)
#           sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), dl//(time.clock() - start)))
#           print()
#     return time.time() - start
#
#
# def check_upload(name):
#   URL = DATA[name] + f"/{name}"
#
#   return URL
#
#
# def main():
#     if len(sys.argv) > 1 :
#         url = sys.argv[1]
#     else :
#         url = input("Enter the URL : ")
#     directory = input("Where would you want to save the file ?")
#
#     time_elapsed = downloadFile(url, directory)
#     print ("Download complete...")
#     print ("Time Elapsed: " + str(time_elapsed))
#
#
# if "__main__" == __name__:
#     t = """[{\"msg_index\":0,\"events\":[{\"type\":\"message\",\"attributes\":[{\"key\":\"action\",\"value\":\"/greenfield.storage.MsgSealObject\"},{\"key\":\"sender\",\"value\":\"0xE4F1Ac4B9312724D2819347c5c91252b650C4AEb\"},{\"key\":\"module\",\"value\":\"storage\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0xab7f667b18C4a23F4E1ac2E8B3cE05c665F656ce\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"5513393049984000\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"6984154368000\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"-354513442\\\"\"},{\"key\":\"out_flows\",\"value\":\"[{\\\"to_address\\\":\\\"0x05e10816F92aB9aE545733db2f73bB858F9DC1fa\\\",\\\"rate\\\":\\\"45389174\\\"},{\\\"to_address\\\":\\\"0x34C78a5BCC1b0fD7F58E4f36393d29A356603698\\\",\\\"rate\\\":\\\"45389174\\\"},{\\\"to_address\\\":\\\"0x4B956d53E466a53d5FdE86781F1f547B44a19260\\\",\\\"rate\\\":\\\"45273034\\\"},{\\\"to_address\\\":\\\"0x8FeD9Ba853B685c2e482DEba08cE30F6942A9F2f\\\",\\\"rate\\\":\\\"45389174\\\"},{\\\"to_address\\\":\\\"0xD3af86C62D53dA3aD7FD3eaF867D91E1Ba9c61AC\\\",\\\"rate\\\":\\\"45389174\\\"},{\\\"to_address\\\":\\\"0xE44c4e725598CCa7Da3c506869d658a84e599983\\\",\\\"rate\\\":\\\"45424406\\\"},{\\\"to_address\\\":\\\"0xd641C35f947Eb60676f0e0793691bB174256C651\\\",\\\"rate\\\":\\\"78633133\\\"},{\\\"to_address\\\":\\\"0xdF5F0588f6B09f0B9E58D3426252db25Dc74E7a1\\\",\\\"rate\\\":\\\"3510033\\\"},{\\\"to_address\\\":\\\"0xf052f6A8e05C1dD7FEbc987dd4BBA1D33BF52200\\\",\\\"rate\\\":\\\"116140\\\"}]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"1700597315\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"3490304616790\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"coin_spent\",\"attributes\":[{\"key\":\"spender\",\"value\":\"0xab7f667b18C4a23F4E1ac2E8B3cE05c665F656ce\"},{\"key\":\"amount\",\"value\":\"36702359210BNB\"}]},{\"type\":\"coin_received\",\"attributes\":[{\"key\":\"receiver\",\"value\":\"0x040fFD5925D40E11c67b7238A7fc9957850B8b9a\"},{\"key\":\"amount\",\"value\":\"36702359210BNB\"}]},{\"type\":\"transfer\",\"attributes\":[{\"key\":\"recipient\",\"value\":\"0x040fFD5925D40E11c67b7238A7fc9957850B8b9a\"},{\"key\":\"sender\",\"value\":\"0xab7f667b18C4a23F4E1ac2E8B3cE05c665F656ce\"},{\"key\":\"amount\",\"value\":\"36702359210BNB\"}]},{\"type\":\"message\",\"attributes\":[{\"key\":\"sender\",\"value\":\"0xab7f667b18C4a23F4E1ac2E8B3cE05c665F656ce\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0xab7f667b18C4a23F4E1ac2E8B3cE05c665F656ce\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"5516920056960000\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"6984154368000\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"-354740230\\\"\"},{\"key\":\"out_flows\",\"value\":\"[{\\\"to_address\\\":\\\"0x05e10816F92aB9aE545733db2f73bB858F9DC1fa\\\",\\\"rate\\\":\\\"45418209\\\"},{\\\"to_address\\\":\\\"0x34C78a5BCC1b0fD7F58E4f36393d29A356603698\\\",\\\"rate\\\":\\\"45418209\\\"},{\\\"to_address\\\":\\\"0x4B956d53E466a53d5FdE86781F1f547B44a19260\\\",\\\"rate\\\":\\\"45302069\\\"},{\\\"to_address\\\":\\\"0x8FeD9Ba853B685c2e482DEba08cE30F6942A9F2f\\\",\\\"rate\\\":\\\"45418209\\\"},{\\\"to_address\\\":\\\"0xD3af86C62D53dA3aD7FD3eaF867D91E1Ba9c61AC\\\",\\\"rate\\\":\\\"45418209\\\"},{\\\"to_address\\\":\\\"0xE44c4e725598CCa7Da3c506869d658a84e599983\\\",\\\"rate\\\":\\\"45453441\\\"},{\\\"to_address\\\":\\\"0xd641C35f947Eb60676f0e0793691bB174256C651\\\",\\\"rate\\\":\\\"78683465\\\"},{\\\"to_address\\\":\\\"0xdF5F0588f6B09f0B9E58D3426252db25Dc74E7a1\\\",\\\"rate\\\":\\\"3512279\\\"},{\\\"to_address\\\":\\\"0xf052f6A8e05C1dD7FEbc987dd4BBA1D33BF52200\\\",\\\"rate\\\":\\\"116140\\\"}]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"1700587470\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0x05e10816F92aB9aE545733db2f73bB858F9DC1fa\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"507369305\\\"\"},{\"key\":\"out_flows\",\"value\":\"[]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"0\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"26867520966880\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0x34C78a5BCC1b0fD7F58E4f36393d29A356603698\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"521889854\\\"\"},{\"key\":\"out_flows\",\"value\":\"[]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"0\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"27275117562868\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0x4B956d53E466a53d5FdE86781F1f547B44a19260\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"571058660\\\"\"},{\"key\":\"out_flows\",\"value\":\"[]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"0\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"28795650099288\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0x8FeD9Ba853B685c2e482DEba08cE30F6942A9F2f\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"577095463\\\"\"},{\"key\":\"out_flows\",\"value\":\"[]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"0\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"29519397474613\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0xD3af86C62D53dA3aD7FD3eaF867D91E1Ba9c61AC\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"627644298\\\"\"},{\"key\":\"out_flows\",\"value\":\"[]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"0\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"36181006868163\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0xE44c4e725598CCa7Da3c506869d658a84e599983\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"569138053\\\"\"},{\"key\":\"out_flows\",\"value\":\"[]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"0\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"28740784808352\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0xd641C35f947Eb60676f0e0793691bB174256C651\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"762091696\\\"\"},{\"key\":\"out_flows\",\"value\":\"[]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"0\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"32684054638240\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"greenfield.payment.EventStreamRecordUpdate\",\"attributes\":[{\"key\":\"account\",\"value\":\"\\\"0xdF5F0588f6B09f0B9E58D3426252db25Dc74E7a1\\\"\"},{\"key\":\"buffer_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"crud_timestamp\",\"value\":\"\\\"1685121870\\\"\"},{\"key\":\"lock_balance\",\"value\":\"\\\"0\\\"\"},{\"key\":\"netflow_rate\",\"value\":\"\\\"41607105\\\"\"},{\"key\":\"out_flows\",\"value\":\"[]\"},{\"key\":\"settle_timestamp\",\"value\":\"\\\"0\\\"\"},{\"key\":\"static_balance\",\"value\":\"\\\"103441660015\\\"\"},{\"key\":\"status\",\"value\":\"\\\"STREAM_ACCOUNT_STATUS_ACTIVE\\\"\"}]},{\"type\":\"greenfield.storage.EventSealObject\",\"attributes\":[{\"key\":\"bucket_name\",\"value\":\"\\\"zkbridge-05\\\"\"},{\"key\":\"object_id\",\"value\":\"\\\"8333\\\"\"},{\"key\":\"object_name\",\"value\":\"\\\"87aa89ce1e50bf0e2000a838cc6779da\\\"\"},{\"key\":\"operator\",\"value\":\"\\\"0xE4F1Ac4B9312724D2819347c5c91252b650C4AEb\\\"\"},{\"key\":\"secondary_sp_addresses\",\"value\":\"[\\\"0x7715d0680fE84cA6d7eaEF6e8A7CAcE29a4C0064\\\",\\\"0xC6fA3F3640e3b594335efAb349abdD4A82C83736\\\",\\\"0x5E340C0721bD5f49627e7E34eb94bedfA575E993\\\",\\\"0x3CFC8b2095DA8F0722412Dc16f8A067942d2c697\\\",\\\"0xB573F5c174f33aF0CA033c8A287061C1538fb130\\\",\\\"0xE42B5AD90AfF1e8Ad90F76e02541A71Ca9D41A11\\\"]\"},{\"key\":\"status\",\"value\":\"\\\"OBJECT_STATUS_SEALED\\\"\"}]}]}]"""
#
#     t = t.replace("\\", "")
#     print(t)
#     # main()