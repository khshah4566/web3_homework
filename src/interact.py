from web3 import Web3
import json
import os

with open("../build/compiled_code.json", "r") as file:
    compiled_sol = json.load(file)

abi = compiled_sol["contracts"]["newContract.sol"]["newContract"]["abi"]

w3 = Web3(Web3.HTTPProvider(os.getenv("LOCAL_PROVIDER")))
account = os.getenv("ANVIL_ACCOUNT")
private_key = os.getenv("PRIVATE_KEY")

contract_address = input("Enter deployed contract address: ")
contract = w3.eth.contract(address=contract_address, abi=abi)

nonce = w3.eth.get_transaction_count(account)

transaction = contract.functions.updateID(5341).build_transaction({
    "chainId": 31337,
    "from": account,
    "nonce": nonce,
    "gas": 6721975,
    "gasPrice": w3.to_wei("20", "gwei")
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print("Updating StudentID...")

txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

updated_value = contract.functions.viewMyId().call()

print(f"Updated value is {updated_value}")
