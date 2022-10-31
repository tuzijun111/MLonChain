# ML on Chain Project

1. The ML models folder contains three ML models which are implemented in C++. This is because the SGX-based method is more compatible to C++ programs. Therefore, for consistency, we use the same ML models in C++ for all the off-chain running time evaluation.

2. The off-chain Comparison folder contains the implementation of the five off-chain methods.

3. The SC interaction folder includes the programs for calling the corresponding smart contracts (which implemente the ML models in solidity). Also, it contains the program for getting access to the verifier smart contract for the zk-SNARKs-based (in ZoKrates) method. The SGX-based method is implemented with Eclipse on the Ubuntu 20.04.

4. The Smart Contracts folder contain all the smart contracts which implement ML models, inference and updating. The ZoKrates will generate a specific verifier function for each new setting of ML models, therefore, we do not include the verifier smart contracts here.

5. The Dataset folder contains two real datasets: Amazon Access Samples and 3D Road Network.
