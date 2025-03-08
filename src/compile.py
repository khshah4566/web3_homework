from solcx import compile_standard
import json

def compile_contract():
    with open("src\Contract.sol", "r") as file:
        contract_source_code = file.read()
    
    compiled_sol = compile_standard(
            {
            "language": "Solidity",
            "sources": {"Contract.sol": {"content": contract_source_code}},
            "settings": {
                "outputSelection": {
                    "": {"": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.13",
    )
    
    # Save the compiled output
    with open("compiled_contract.json", "w") as file:
        json.dump(compiled_sol, file)
    
    print("Contract compiled successfully!")
    return compiled_sol

if __name__ == "__main__":
    print("running")
    compile_contract()