from   web3.middleware import geth_poa_middleware
from   web3            import Web3,HTTPProvider
import web3
import json
import asyncio



#### Basic Functions ####
def readfile(p):
	with open(p, 'r') as f:
		return f.read()



#### Init Web3 #### 
w3 = Web3(HTTPProvider(r"https://rinkeby.infura.io/v3/8155419f25ce4de090fcac6c96411c24"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)



#### Prepare Wallet ####
account_addr  = "0x2611a07982139d9b661bF5f6c15FB79EaDc4D936"
encrypted_key = readfile("../../wallet/EGGProvider.key")
pwsd          = readfile("../../wallet/pswd.txt")
private_key   = w3.eth.account.decrypt(encrypted_key, pwsd)



#### Prepare Contract ####
contract_addr = readfile("../Contracts/TwistEGG-Random-Framwork-v1.5-t-address-Rinkeby.txt")
contract_abi  = readfile("../Contracts/TwistEGG-Random-Framwork-v1.5-t-abi.txt")
contract_abi  = json.loads(contract_abi)
myContract    = w3.eth.contract(address=contract_addr, abi=contract_abi)



#### Functions ####
def solidity_keccak256(dtype, value):
	return Web3.solidityKeccak([dtype], [value]).hex()


def gatNonce(account_addr):
	return w3.eth.getTransactionCount(account_addr)


def formTXPrams(account_addr):
	return {'from': account_addr, 'nonce': gatNonce(account_addr)}


def getIDX():
	head = myContract.functions.head().call()
	mid  = myContract.functions.mid().call()
	tail = myContract.functions.tail().call()

	return head, mid, tail


def getOrder(idx):
	return myContract.functions.Orders(idx).call()


def getBalance(address):
	balance_wei = w3.eth.get_balance(account_addr)
	balance     = balance_wei / (10 ** 18)

	return balance



#### Contract Functions ####
def ContractFRequest(_a):
	RequestF   = myContract.functions.Request(_a).buildTransaction(formTXPrams(account_addr))
	signed_txn = w3.eth.account.signTransaction(RequestF, private_key)
	txReport   = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	return txReport.hex()


def ContractFPrepare(_hashB):
	RequestF   = myContract.functions.Prepare(_hashB).buildTransaction(formTXPrams(account_addr))
	signed_txn = w3.eth.account.signTransaction(RequestF, private_key)
	txReport   = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	return txReport.hex()


def ContractFVerify(_b):
	RequestF   = myContract.functions.Verify(_b).buildTransaction(formTXPrams(account_addr))
	signed_txn = w3.eth.account.signTransaction(RequestF, private_key)
	txReport   = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	return txReport.hex()


def ContractFSetPause(_state):
	RequestF   = myContract.functions.Verify(_state).buildTransaction(formTXPrams(account_addr))
	signed_txn = w3.eth.account.signTransaction(RequestF, private_key)
	txReport   = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	return txReport.hex()	



#### Event Listner Functions ####
def handle_event(event):
    print(event)


async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)


def EventsListener():
    event_filter = myContract.events.atest.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2),
                #log_loop(tx_filter, 2)
                ))
    finally:
        loop.close()



#### Print ####
print("Wallet:"   , account_addr)
print("Balance:"  , getBalance(account_addr))
print("nonce:"    , gatNonce(account_addr))
print("Contract:" , contract_addr)
print("Index:"    , getIDX())



#### Main Function ####
if __name__ == '__main__':
    EventsListener()













