from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def interact_with_contract(contract_address):
    with open("compiled_contract.json", "r") as file:
        compiled_contract = json.load(file)

    abi = compiled_contract["contracts"]["newContract.sol"]["newContract"]["abi"]

    w3 = Web3(Web3.HTTPProvider(os.getenv("LOCAL_PROVIDER")))
    account = os.getenv("ANVIL_ACCOUNT")
    private_key = os.getenv("ANVIL_PRIVATE_KEY")

    contract = w3.eth.contract(address=contract_address, abi=abi)

    # Update ID to 5341
    nonce = w3.eth.get_transaction_count(account)
    transaction = contract.functions.updateID(5341).build_transaction({
        "from": account,
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "chainId": 31337
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(txn_hash)

    # Get updated value
    updated_value = contract.functions.viewMyId().call()
    print(f"Updated value is {updated_value}")

if _name_ == "_main_":
    contract_address = input("Enter the deployed contract address: ")
    interact_with_contract(contract_address)