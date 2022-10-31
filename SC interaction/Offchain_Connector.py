from web3 import Web3, HTTPProvider
import web3
import json
import datetime

class RopEth():
    def __init__(self):
        API_URL = "https://goerli.infura.io/v3/88e080f6cca34d0895a6a8f7fe1c00a6"
        PRIVATE_KEY = "7865c3bdd68113e704cea5a8fb002fda782005ab1a4680a7fbae31f01d320eb3"
        PUBLIC_KEY = "0x4f165218486CAE53022802701882b52d108076C3"
        # 0xe6bBAC8898BDF8Fc8431C905369AA96a7AEBfb62  with emit events
        # 0x137651cdA9685eb1DB09AA25a51ee9E17Abf659D without emit events
        self.contract_address = "0xB1F80a04Ad528A130724ac85612Cb341a99aFAc6"
        
        self.wallet_private_key = PRIVATE_KEY
        self.wallet_address = PUBLIC_KEY
        self.w3 = Web3(HTTPProvider(API_URL))
        with open('contracts/Offchain.json') as f:
            self.data = json.load(f)
            # print("Contract ABI: ",self.data["abi"])
            self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.data["abi"])

    def model_coeff_get(self, s1, s2, m):
        # Executing a transaction.
        nonce = self.w3.eth.get_transaction_count(self.wallet_address)
    
        estimatedGas = self.contract.functions.update(s1, s2, m).estimateGas()
        # print("Estimated gas to execute the transaction: ",estimatedGas)
        # print(dir(self.contract.functions.update(message)))
        txn_dict = self.contract.functions.update(s1, s2, m).buildTransaction({
            'gas': estimatedGas,
            'from': self.wallet_address,
            'nonce': nonce,
        })
        print("estimated gas is", estimatedGas)
        # print(dir(self.w3.eth.account))
        signPromise = self.w3.eth.account.signTransaction(txn_dict, self.wallet_private_key)
        # print(dir(signPromise))
        # result = self.w3.eth.send_raw_transaction(signPromise.rawTransaction)
        return estimatedGas

    def network_update(self, s1, s2, m):
        # Executing a transaction.
        nonce = self.w3.eth.get_transaction_count(self.wallet_address)
    
        estimatedGas = self.contract.functions.twod_update(s1, s2, m).estimateGas()
        # print("Estimated gas to execute the transaction: ",estimatedGas)
        # print(dir(self.contract.functions.update(message)))
        txn_dict = self.contract.functions.twod_update(s1, s2, m).buildTransaction({
            'gas': estimatedGas,
            'from': self.wallet_address,
            'nonce': nonce,
        })
        print("estimated gas is", estimatedGas)
        # print(dir(self.w3.eth.account))
        signPromise = self.w3.eth.account.signTransaction(txn_dict, self.wallet_private_key)
        # print(dir(signPromise))
        # result = self.w3.eth.send_raw_transaction(signPromise.rawTransaction)
        return estimatedGas

    def sim_cost_get(self, m):
        # Executing a transaction.
        nonce = self.w3.eth.get_transaction_count(self.wallet_address)
    
        estimatedGas = self.contract.functions.sim_compute(m).estimateGas()
        # print("Estimated gas to execute the transaction: ",estimatedGas)
        # print(dir(self.contract.functions.update(message)))
        txn_dict = self.contract.functions.sim_compute(m).buildTransaction({
            'gas': estimatedGas,
            'from': self.wallet_address,
            'nonce': nonce,
        })
        print("sim_compute estimated gas is", estimatedGas)
        # print(dir(self.w3.eth.account))
        signPromise = self.w3.eth.account.signTransaction(txn_dict, self.wallet_private_key)
        # print(dir(signPromise))
        # result = self.w3.eth.send_raw_transaction(signPromise.rawTransaction)
        return estimatedGas

    def result_get(self, s1, s2, m):
        v = self.contract.functions.update(s1, s2, m).call()
        # w = self.contract.functions.simple_linear_regression().call() 
        #print(dir(self.contract.functions()))
        print("The model is ", v)
        # print("The prediction for the first 5 items: ", w)
        
    


if __name__ == '__main__':
    r =RopEth()
    #r.model_coeff_get()
    s1 = "A"
    # s2 = "[]"
    s2 = "B"
    # for i in range(50):
    #     s2 += "A" 
    # print(s2)
    y = []
    # m = [1 for i in range(10)]
    
    # r.model_coeff_get(s1, s2, m)

    
    # for i in range(10, 101, 10):
    #     dataset = [[1 for i in range(i)] for j in range(9)]
    #     res = r.sim_cost_get(dataset)
    #     y.append(res)
    # print(y)
    
    def model_update_cost():
        for i in range(200, 201):
        # for i in range(100, 9, -10):
            m = [1 for i in range(i)]
            res = r.model_coeff_get(s1, s2, m)
            y.append(res)
        print(y)
    
    def network_update_cost():
        for i in range(4, 5, 10):
            m = [[1 for i in range(4)] for j in range(2)]
            
            y.append(r.network_update(s1, s2, m))
        print(y)
    
    network_update_cost()
    
 