from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def deploy_contract():
    with open("compiled_contract.json", "r") as file:
        compiled_contract = json.load(file)

    abi = compiled_contract["contracts"]["newContract.sol"]["newContract"]["abi"]
    bytecode = compiled_contract["contracts"]["newContract.sol"]["newContract"]["evm"]["bytecode"]["object"]

    w3 = Web3(Web3.HTTPProvider(os.getenv("LOCAL_PROVIDER")))
    account = os.getenv("ANVIL_ACCOUNT")
    private_key = os.getenv("ANVIL_PRIVATE_KEY")

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(account)
    transaction = contract.constructor().build_transaction({
        "from": account,
        "nonce": nonce,
        "gas": 6721975,
        "gasPrice": w3.to_wei("20", "gwei"),
        "chainId": 31337
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    print(f"Contract deployed at {txn_receipt.contractAddress}")
    return txn_receipt.contractAddress

if _name_ == "_main_":
    deploy_contract()