from solcx import compile_standard, install_solc
import json

install_solc("0.8.13")

with open("../contracts/newContract.sol", "r") as file:
    contract_source_code = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"newContract.sol": {"content": contract_source_code}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.13",
)

with open("../build/compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

print("Contract compiled successfully!")