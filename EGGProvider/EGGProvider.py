from   web3.middleware import geth_poa_middleware
from   web3            import Web3,HTTPProvider
from   time            import sleep
import csv
import web3
import json
import asyncio
import secrets



#### Basic Functions ####
def readfile(p):
	with open(p, 'r') as f:
		return f.read()

def writefile(p, c):
	with open(p, 'w') as f:
		f.write(str(c))



#### Init Web3 #### 
w3 = Web3(HTTPProvider(r"https://rinkeby.infura.io/v3/8155419f25ce4de090fcac6c96411c24"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)



#### Prepare Wallet ####
account_addr  = "0x2611a07982139d9b661bF5f6c15FB79EaDc4D936"
encrypted_key = readfile("../../wallet/EGGProvider.key")
pwsd          = readfile("../../wallet/pswd.txt")
private_key   = w3.eth.account.decrypt(encrypted_key, pwsd)



#### Prepare Contract ####
contract_addr = readfile("../Contracts/TwistEGG-Random-Framwork-v1.5.2-t-address-Rinkeby.txt")
contract_abi  = readfile("../Contracts/TwistEGG-Random-Framwork-v1.5.2-t-abi.txt")
contract_abi  = json.loads(contract_abi)
myContract    = w3.eth.contract(address=contract_addr, abi=contract_abi)
writefile("nonce.txt", w3.eth.getTransactionCount(account_addr))



#### Setting ####
SAFESPACE = 4



#### Functions ####
def solidity_keccak256(dtype, value):
	return Web3.solidityKeccak([dtype], [value]).hex()


def gatNonce(account_addr):
	return w3.eth.getTransactionCount(account_addr)


def formTXPrams(account_addr):
	NONCE = int(readfile("nonce.txt"))
	writefile("nonce.txt", NONCE+1)
	return {"gasPrice": w3.eth.gas_price, "chainId": 4, 'from': account_addr, 'nonce': NONCE}


def getIDX():
	head = myContract.functions.head().call()
	mid  = myContract.functions.mid().call()
	tail = myContract.functions.tail().call()

	return head, mid, tail


def getHeadIDX():
	head = myContract.functions.head().call()

	return head


def getMidIDX():
	mid  = myContract.functions.mid().call()

	return mid


def getTailIDX():
	tail = myContract.functions.tail().call()

	return tail


def InitIDX():
	head = getHeadIDX()
	tail = getTailIDX()
	writefile("HeadIDX.txt", head)
	writefile("TailIDX.txt", tail)


def InitNonce():
	writefile("nonce.txt", w3.eth.getTransactionCount(account_addr))

	
def getCorrectHeadIDX():
	head = int(readfile("HeadIDX.txt"))
	writefile("HeadIDX.txt", head+1)

	return head


def getCorrectTailIDX():
	tail = int(readfile("TailIDX.txt"))
	writefile("TailIDX.txt", tail+1)

	return tail


def getOrder(idx):
	# [b'Ui\x04G\x19\xa1\xec;\x04\xd0\xaf\xa9\xe7\xa51\x0c|\x04s3\x1d\x13\xdc\x9f\xaf\xe1C\xb2\xc4\xe8\x14\x8a', 777, 123, 55360806276233881699509444385957755009136266327774278027399501919756178362338]
	# 0:hashB
	# 1:A
	# 2:B
	# 3:R
	return myContract.functions.Orders(idx).call()


def getBalance(address):
	balance_wei = w3.eth.get_balance(account_addr)
	balance     = balance_wei / (10 ** 18)

	return balance


def CHKBabyContract():
	head = getHeadIDX()
	if head == 0:
		with open("hashB_Pairs.csv", "w") as f:
			f.write("")



def SyncOnChain():
	InitIDX()
	InitIDX()
	CHKBabyContract()



#### Contract Functions ####
def ContractFRequest(_a):
	RequestF   = myContract.functions.Request(_a).buildTransaction(formTXPrams(account_addr))
	signed_txn = w3.eth.account.signTransaction(RequestF, private_key)
	txReport   = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	return txReport.hex()


def ContractFPrepare(_hashB):
	PrepareF   = myContract.functions.Prepare(_hashB).buildTransaction(formTXPrams(account_addr))
	signed_txn = w3.eth.account.signTransaction(PrepareF, private_key)
	txReport   = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	return txReport.hex()


def ContractFVerify(_b):
	VerifyF    = myContract.functions.Verify(_b).buildTransaction(formTXPrams(account_addr))
	signed_txn = w3.eth.account.signTransaction(VerifyF, private_key)
	txReport   = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	return txReport.hex()


def ContractFVerifyByIDX(idx, _b):
	VerifyByIDXF = myContract.functions.VerifyByIDX(idx, _b).buildTransaction(formTXPrams(account_addr))
	signed_txn  = w3.eth.account.signTransaction(VerifyByIDXF, private_key)
	txReport    = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	return txReport.hex()


def ContractFSetPause(_state):
	setPauseF  = myContract.functions.setPause(_state).buildTransaction(formTXPrams(account_addr))
	signed_txn = w3.eth.account.signTransaction(setPauseF, private_key)
	txReport   = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

	return txReport.hex()



#### Functions ####
def generateHashBPair():
	B = secrets.token_hex(32)
	B = int(B, 16)
	hashB = solidity_keccak256("uint256", B)

	return B, hashB


def SAVEhashBPair(idx, B, hashB):
	pair = ','.join([str(idx), str(B), hashB]) + '\n'
	with open("hashB_Pairs.csv", 'a') as f:
		f.write(pair)


def SEARCHhashBPair(idx, hashB):
	pairs = []
	with open("hashB_Pairs.csv", newline='') as csvfile:
		pairs = csv.reader(csvfile)
		for p in pairs:
			if p[0] == str(idx):
				B = int(p[1])
				_hashB = p[2]
				if hashB != _hashB:
					print("Unmatch hashB:")
					print("hashB on chain:", hashB)
					print("hashB on loacl:", _hashB)

				return B
		print("index not found")


def ContractFPrepareMany(times):
	print("ContractFPrepareMany(%s)"%(times))
	for _ in range(int(times)):
		B, hashB = generateHashBPair()
		print("hashB Pair:\n", str(B)+"\n", hashB)
		headIDX = getCorrectHeadIDX()
		print("Prepare(%s):"%hashB, ContractFPrepare(hashB))
		SAVEhashBPair(headIDX, B, hashB)


def PrepareHashB(safe_space):
	print("PrepareHashB(%s):"%(safe_space))
	space = getHeadIDX() - getMidIDX()
	if space == 0:
		ContractFPrepareMany(safe_space)
	elif space <= safe_space/2:
		ContractFPrepareMany(safe_space/2)


def CHKandVerify(targetIDX):
	tailIDX = getTailIDX()
	print("CHKandVerify(): %d to %d"%(tailIDX, targetIDX))
	if tailIDX >= targetIDX:
		print("GOout: tailIDX >= targetIDX")
		return
	for idx in range(tailIDX, targetIDX):
		Order = getOrder(idx)
		if Order[2] == 0:
			hashB = "0x" + Order[0].hex()
			print("SEARCHhashBPair(%s, %s)"%(idx, hashB))
			B = SEARCHhashBPair(idx, hashB)	
			print("Find B:", B)
			idx = getCorrectTailIDX()
			print("ContractFVerifyByIDX(%d, %d):"%(idx, B), ContractFVerifyByIDX(idx, B))
			# print("ContractFVerify(%d):"%B, ContractFVerify(B))








#### Event Listner Functions ####
def handle_event(event):
	# READ(B)
	print("Recive Recipt:")
	print(event)
	print(event['args'])
	print(event['args']['Order_ID'])
	idx   = event['args']['Order_ID']
	hashB = event['args']['EGG_Provider_Chosen_Number_Hash']
	CHKandVerify(idx+1)
	PrepareHashB(SAFESPACE)

	'''
	print("SEARCHhashBPair(%s, %s)"%(idx, hashB))
	B = SEARCHhashBPair(idx, hashB)	
	print("Find B:", B)
	print("ContractFVerify(%s):"%B, ContractFVerify(B))
	'''



def handle_event_test(event):
    print(event)
    # event = [AttributeDict({'args': AttributeDict({'a': 123456}), 'event': 'atest', 'logIndex': 7, 'transactionIndex': 6, 'transactionHash': HexBytes('0xc3df87b8750570a4cd23a6a5b2652185fc653bfc0d07643ed2a5803e1077eedd'), 'address': '0x687803bD9e5a9C9dD60B913FB26FC84CC0B1C7B4', 'blockHash': HexBytes('0xf05b1c0be90001bfdc93adae8e8c6ab75370a187e6b9e34255c1ac34ca1ada25'), 'blockNumber': 10726023})]


async def log_loop(event_filter, poll_interval):
    while True:
    	# head_control() #Prepare
    	# hashB_store

        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)


def EventsListener():
	print("Listning Receipt Events.....")
	# event_filter = myContract.events.atest.createFilter(fromBlock='latest')
	event_filter = myContract.events.Receipt.createFilter(fromBlock='latest')
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(
			asyncio.gather(
				log_loop(event_filter, 2),
				#log_loop(handle_event_test, 2)
				))
	finally:
		loop.close()



#### Print ####
print("Wallet:"   , account_addr)
print("Balance:"  , getBalance(account_addr))
print("nonce:"    , gatNonce(account_addr))
print("Contract:" , contract_addr)
print("Index:"    , getIDX())
print("SAFESPACE:", SAFESPACE)



#### Main Function ####
if __name__ == '__main__':
	SyncOnChain()
	PrepareHashB(SAFESPACE)
	CHKandVerify(getMidIDX())
	EventsListener()












