from web3 import Web3,HTTPProvider
import web3
from web3.middleware import geth_poa_middleware
import json

def readfile(p):
	with open(p, 'r') as f:
		return f.read()

def solidity_keccak256(dtype, value):
	return Web3.solidityKeccak([dtype], [value]).hex()



contract_addr = readfile("../Contracts/TwistEGG-Random-Framwork-v1.5-address-Rinkeby.txt")
contract_abi = readfile("../Contracts/TwistEGG-Random-Framwork-v1.5-abi.txt")
contract_abi = json.loads(contract_abi)

w3 = Web3(HTTPProvider(r"https://rinkeby.infura.io/v3/8155419f25ce4de090fcac6c96411c24"))
print(w3.eth.blockNumber)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
myContract = w3.eth.contract(address="0xfb5A6e6e08a7f2875F70d5954a3F4d7d0F4d9D86", abi=contract_abi)
head = myContract.functions.head().call()
mid = myContract.functions.mid().call()
tail = myContract.functions.tail().call()
print(myContract)

account_addr = "0x2611a07982139d9b661bF5f6c15FB79EaDc4D936"
encrypted_key = readfile("../../wallet/EGGProvider.key")
pwsd = readfile("../../wallet/pswd.txt")
private_key = w3.eth.account.decrypt(encrypted_key, pwsd)

nonce = w3.eth.getTransactionCount(account_addr)
print(nonce)

balance_wei = w3.eth.get_balance(account_addr)
balance = balance_wei / (10 ** 18)

print(balance)


tx_params = {
    #'gas': 1000000, # gas limit, 單位為 gas
    #'value': 1 * (10 ** 18), # 要傳送的 ETH 數目
    #'gasPrice': infuraProvider_ropsten.toWei('2', 'gwei'), # 願意支付的 gas fee 價格 (我們願意支付 2 gwei for each gas)
    'from': account_addr, # signer（就是我們）
    'nonce': nonce # nonce of signer（輸入剛剛獲得的 nonce）
}
print(tx_params)

'''
RequestF = myContract.functions.Request(99877).buildTransaction(tx_params)

signed_txn = w3.eth.account.signTransaction(RequestF, private_key)
txReport = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(signed_txn)
print(txReport.hex())
'''


print(head, mid, tail)
print(myContract.address)
print(myContract.all_functions())
print(myContract.functions.RANDOM(123).call().hex())
print(w3.solidityKeccak(['uint256'], [123]).hex())
print(solidity_keccak256('uint256', 123))
print(myContract.functions.Orders(10).call())
#print(myContract.functions.Request(123456).transact())




