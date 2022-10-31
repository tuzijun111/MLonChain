from time import sleep
from web3 import Web3, HTTPProvider
import web3
import json
import datetime
import numpy as np
import copy
import pickle
import random
import csv

class RopEth():
    def __init__(self):
        # API_URL = "https://eth-ropsten.alchemyapi.io/v2/evXrvWnkYCOBdpZClctchytALhw50T_7"
        API_URL = "https://goerli.infura.io/v3/88e080f6cca34d0895a6a8f7fe1c00a6"
        PRIVATE_KEY = "7865c3bdd68113e704cea5a8fb002fda782005ab1a4680a7fbae31f01d320eb3"
        PUBLIC_KEY = "0x4f165218486CAE53022802701882b52d108076C3"
        # self.contract_address = "0x5864d7930A7E822b131ea316b57190056175907E"  #NN prediction
        self.contract_address = "0xbEef28770Ad18C1D5Ec29345b63d41842987A17D"  #NN model 
        self.wallet_private_key = PRIVATE_KEY
        self.wallet_address = PUBLIC_KEY
        self.w3 = Web3(HTTPProvider(API_URL))
        with open('contracts/NeuralNetwork.json') as f:
            self.data = json.load(f)
            # print("Contract ABI: ",self.data["abi"])
            self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.data["abi"])

    def model_gas_cost(self, network, train, label, l_rate, n_epoch, n_outputs):
        # Executing a transaction.
        nonce = self.w3.eth.get_transaction_count(self.wallet_address)
    
        estimatedGas1 = self.contract.functions.train_network(network, train, label, l_rate, n_epoch, n_outputs).estimateGas()
        
        # print("Estimated gas to execute the transaction: ",estimatedGas)
        # print(dir(self.contract.functions.update(message)))
        txn_dict = self.contract.functions.train_network(network, train, label, l_rate, n_epoch, n_outputs).buildTransaction({
            'gas': estimatedGas1,
            'from': self.wallet_address,
            'nonce': nonce,
        })
        print("gas for the whole model:", estimatedGas1)
        
        # # Need to sign to generate the transaction. Otherwise, we can not generate transactions on etherscan.
        # signPromise = self.w3.eth.account.signTransaction(txn_dict, self.wallet_private_key)
        # # Return the transaction hashvalue
        # result = self.w3.eth.send_raw_transaction(signPromise.rawTransaction)
        
        return estimatedGas1

    # since we can not train the model with large size dataset, we need to incrementally train the model
    # At each round, we feed the model with a part of the dataset

    def prediction_cost(self, network, row):
        # Executing a transaction.
        nonce = self.w3.eth.get_transaction_count(self.wallet_address)
    
        estimatedGas1 = self.contract.functions.predict(network, row).estimateGas()
        # print("Estimated gas to execute the transaction: ",estimatedGas)
        # print(dir(self.contract.functions.update(message)))
        txn_dict = self.contract.functions.predict(network, row).buildTransaction({ # prediction for a single item
            'gas': estimatedGas1,
            'from': self.wallet_address,
            'nonce': nonce,
        })
        print("gas for prediction:", estimatedGas1)
        
        # # Need to sign to generate the transaction. Otherwise, we can not generate transactions on etherscan.
        # signPromise = self.w3.eth.account.signTransaction(txn_dict, self.wallet_private_key)
        # # Return the transaction hashvalue
        # result = self.w3.eth.send_raw_transaction(signPromise.rawTransaction)
        
        return estimatedGas1
    

    def getTransactionReciept(self, txnHash):
        try:
            # sleep(400)
            response = self.w3.eth.wait_for_transaction_receipt( txnHash, timeout=120, poll_latency=0.1)
            print("True gas cost:", response)
            return response
        except web3.exceptions.TimeExhausted:
            print("what?")
            return None
        except web3.exceptions.TransactionNotFound:
            print("Something else")
        except Exception as ex:
            print("something other", ex)

    def result_get(self, network, train, label, l_rate, n_epoch, n_outputs):
        v = self.contract.functions.train_network(network, train, label, l_rate, n_epoch, n_outputs).call()
        # w = self.contract.functions.train_network( n_epoch, n_outputs).call()
        #print(dir(self.contract.functions()))
        print("The coefficients are: ", v)
        # print("The predictions are: ", w)
    
    def test_get(self, input):
    #def test_get(self, train, test, l_rate, n_epoch):
        v = self.contract.functions.test3(input).call()
        #v = self.contract.functions.logistic_regression(train, test, l_rate, n_epoch).call()
        print("result: ", v)

   
    def model_run(self, train, test, l_rate, n_epoch):
        v = self.contract.functions.logistic_regression(train, test, l_rate, n_epoch).call()
        print("result: ", v)
      
class MLmodel():
    def __init__(self):
        # the initial parameters of the dataset
        
        self.l_rate = 1*pow(10, 17)
        
        
        #self.model = "Neurual Network"

    def num_of_input(self, dataset, num_input, num_epoch):
        X = []
        Y = []
        r =RopEth()    
        # get the gas cost of the model with different (consecutive) parameters
        for k in range(self.num_input, num_input+1, 20):       
            # get the train dataset from the big dataset based on a specified number of features
            train = []
            test = []
            for i in range(k): 
                # train.append([])    
                train.append(dataset[i])   # since we need to add the label column to the dataset, so 
                # the totoal number of an item is k+1           
            for i in range(5):
                # test.append([])
                test.append(dataset[i])
            X.append(k)
            s = r.model_gas_cost(train, test, self.l_rate, num_epoch)
            Y.append(s)        

        return X, Y

    def num_of_input_run(self, dataset, num_input, num_epoch):
        X, Y = self.num_of_input(dataset, num_input, num_epoch)
        # store the X values into a .txt file
        a_file = open("input_X.txt", "w")  
        np.savetxt(a_file, X)
        a_file.close()
        # store the Y values into a .txt file
        a_file = open("input_Y.txt", "w")
        np.savetxt(a_file, Y)
        a_file.close()


    # return the data with different parameters. num_feature, num_input must not be less than them in the initial dataset
    # since we use the initial dataset as a basicline to augment the dataset
    def num_of_feature(self, dataset, num_feature, num_epoch):
        X = []
        Y = []
        r =RopEth()
        # get the gas cost of the model with different (consecutive) parameters
        for k in range(self.num_feature, num_feature+1, 5):       
            # get the train dataset from the big dataset based on a specified number of features
            train = []
            test = []
            for i in range(len(dataset)): 
                # train.append([])    
                train.append(dataset[i][0:(k+1)])   # since we need to add the label column to the dataset, so 
                # the totoal number of an item is k+1          
            for i in range(5):
                # test.append([])
                test.append(dataset[i][0:(k+1)]) 
            X.append(k)
            s = r.model_gas_cost(train, test, self.l_rate, num_epoch)
            Y.append(s)        
        return X, Y
    

    def num_of_feature_run(self, dataset, num_feature, num_epoch):
        X, Y = self.num_of_feature(dataset, num_feature, num_epoch)
        # store the X values into a .txt file
        a_file = open("feature_X.txt", "w")  
        np.savetxt(a_file, X)
        a_file.close()
        # store the Y values into a .txt file
        a_file = open("feature_Y.txt", "w")
        np.savetxt(a_file, Y)
        a_file.close()

    def num_of_epoch(self, dataset, num_epoch):
        X = []
        Y = [] 
        r =RopEth()  
        # get the gas cost of the model with different (consecutive) parameters
        for k in range(self.num_epoch, num_epoch+1):
            train = dataset
            test = []     
            for i in range(5):
                # test.append([])
                test.append(dataset[i])
            X.append(k)
            s = r.model_gas_cost(train, test, self.l_rate, k)
            Y.append(s)        
        return X, Y

    def num_of_epoch_run(self, dataset, num_epoch):
        X, Y = self.num_of_epoch(dataset, num_epoch)
        # store the X values into a .txt file
        a_file = open("epoch_X.txt", "w")  
        np.savetxt(a_file, X)
        a_file.close()
        # store the Y values into a .txt file
        a_file = open("epoch_Y.txt", "w")
        np.savetxt(a_file, Y)
        a_file.close()
     
    # run the model without getting a subset of the dataset
    def model_run(self, network, train, label, l_rate, n_epoch, n_outputs):
        r =RopEth()

        r.model_gas_cost(network, train, label, l_rate, n_epoch, n_outputs)

    def incremental_model_run(self, dataset, num_epoch, coef):
        r =RopEth()
        for k in range(0, len(dataset), 400):
            train = dataset[k:(k+400)]
            test = dataset[0:5]
            coef = r.incremental_model_train(train, test, self.l_rate, num_epoch, coef)
        return coef


    def dataset_gen_txt(self, dataset, num_feature, num_input):
        # increase the number of input data
        for i in range(num_input - 1): 
            dataset.append(copy.deepcopy(dataset[0]))
        # increase the number of features for each row
        for i in range(len(dataset)):
            for j in range(num_feature - self.num_feature):
                dataset[i].append(2_7810836*pow(10, 11))
        # return dataset    
        with open('dataset_input1000.txt', 'wb') as fp:
            pickle.dump(dataset, fp)
        # np.savetxt(a_file, dataset, fmt='%s')
        # a_file.close()

    def prediction_test(self, dataset, network):
        r = RopEth()
        for i in range(1, 3):
            item = dataset[i]
            res = r.prediction_cost(network, item)
            print(res)
            

        # store the Y values into a .txt file
        a_file = open("prediction_input_Y.txt", "w")
        np.savetxt(a_file, Y)
        a_file.close()


    # Initialize a network
    def initialize_network(self, n_inputs, n_hidden, n_outputs):
        network = list()
        hidden_layer = [[random.randint(10, 99)*pow(10, 16) for i in range(n_inputs )] for i in range(n_hidden)]
        network.append(hidden_layer)
        output_layer = [[random.randint(10, 99)*pow(10, 16) for i in range(n_hidden )] for i in range(n_outputs)]
        network.append(output_layer)
        return network
       

        

if __name__ == '__main__':
    import numpy as np
       
    l_rate = 1*pow(10, 17)
    n_epoch = 10
    
    n_inputs = 100   # depends on the number of feature of input dataset
    n_layer = 3
    n_outputs = 2
    num_feature = 1

    
    # create a big dataset
    # m.dataset_gen_txt(dataset, num_feature, num_input)
    m = MLmodel()
    r =RopEth()
    
    X = []
    Y = []
    def Road_read():
        with open('/Users/binbingu/Documents/Picture/BcML/ex/dataset/Road.txt', 'r') as f:
            data = []
            for line in f.readlines():
                temp = []
                line = line.replace('\n', '')
                line = line.split(',')
                line = [int(float(x)*10**15) for x in line]
                data.append(line)
        return data

    def Access_read():
        data = []
        with open('/Users/binbingu/Documents/Picture/BcML/ex/dataset/access.csv', newline='') as csvfile:
            read = csv.reader(csvfile, delimiter= ',')
            
            b = False
            for row in read:
                if b == False:
                    b = True
                    continue
                temp = []
                temp.append(int(row[1]))
                temp.append(int(row[2]))
                data.append(temp)
                        
        # print(data)        
        return data

    
    network = [[[1 for i in range(4)] for i in range(2)] for i in range(3)]
    
    # label = [0 for i in range(n_inputs)]
    
    train = [[1 for i in range(4)] for i in range(n_inputs)]

    # train = Road_read()
    # train = Access_read()
    temp = []
    label = [0 for i in range(10)]
    
    num_dataset = len(train)

    def single_data_onchain_training_gas():
        for i in range(0, num_dataset, 10):
            train_temp = train[i:i+10]  
            v = r.model_gas_cost(network, train_temp, label, l_rate, n_epoch, n_outputs)
            temp.append(v)
        print(sum(temp)/len(temp))
    
    single_data_onchain_training_gas()




    def single_data_onchain_verfication_training_gas():
        for i in range(0, num_dataset, 10):
            train = [[1 for i in range(2)] for i in range(i)]
            label = [0 for i in range(i)]
            r.prediction_cost(network, train)

    single_data_onchain_verfication_training_gas()


    

    


    
    
  

    

   


    
