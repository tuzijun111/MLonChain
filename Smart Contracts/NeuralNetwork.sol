// SPDX-License-Identifier: Unlicense
pragma solidity >=0.8.4;

import "https://github.com/tuzijun111/Solidity-Library/blob/main/math-contract/PRBMathSD59x18.sol";



contract NeuralNetwork {
    using PRBMathSD59x18 for int256;
    int256 one = 1e18;
    int256 half = 5e17;

     
    //  Initialize a network
    //  We specify the parameters used in the network
    /*
    *  network: 3-d array;    network[i] is a 2-d array which represents the weights for the i-th layer. 
    Each row of network[i] represents its weigths to the inputs from its previous layer
    *  neuron_ouput: 2-d array; neuron_ouput[i] means the output for the i-th layer (note that the initial input is not regarded as a layer)
    *
    */

    // uint256 n_input, uint256 n_hidden, uint256 n_output
    // function initialize_network (uint256 n_input, uint256 n_hidden, uint256 n_output) public pure returns(int256[][][] memory){
    //     int256[][][] memory network = new int256[][][](2);    // only hidden layer and one output layer therefore 1+1 = 2
    //     //initialize weight for nodes of the hidden layer 
    //     int256[][] memory hidden_weight  = new int256[][](n_hidden);  //
    //     //need a bias for input so here we need n_input+1
    //     int256[] memory row = new int256[](n_input+1);
    //     for (uint j = 0; j < n_input + 1; j++){
    //         row[j] = 1;
    //     }
    //     for (uint i = 0; i < n_hidden; i++){
    //         hidden_weight[i] = row;
    //     }
    //     network[0] = hidden_weight;
    //     //initialize weight for nodes of the hidden layer
    //     int256[][] memory output_weight  = new int256[][](n_output);  //
    //     //need a bias for input so here we need n_input+1
    //     int256[] memory rowx = new int256[](n_hidden);
    //     for (uint j = 0; j < n_hidden; j++){
    //         rowx[j] = 1;
    //     }
    //     for (uint i = 0; i < n_output; i++){
    //         output_weight[i] = rowx;
    //     }
    //     network[1] = output_weight;
    //     return network;      

    //     //initialize weight for nodes of the hidden layer

    // }

    // # Initialize a network
    // def initialize_network(n_inputs, n_hidden, n_outputs):
    // 	network = list()
    // 	hidden_layer = [{'weights':[random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]
    // 	network.append(hidden_layer)
    // 	output_layer = [{'weights':[random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
    // 	network.append(output_layer)
    // 	return network

    
    // # Calculate neuron activation for an input
    // 
    function activate (int256[][] memory weights, int256[] memory input) public pure returns(int256[] memory){
        int256[] memory activation = new int256[](weights.length);
        //initialize all the values in activation array as 0
        for (uint i = 0; i < weights.length; i++){
            activation[i] = 0;
        }
        for (uint i = 0; i < weights.length; i++){
            for (uint j = 0; j < weights[i].length; j++){
                activation[i] = activation[i] + PRBMathSD59x18.mul(weights[i][j], input[j]);
            }
        }
        return activation;
    }

    
    // def activate(weights, inputs):
    // 	activation = weights[-1]
    // 	for i in range(len(weights)-1):
    // 		activation += weights[i] * inputs[i]
    // 	return activation


    // # Transfer neuron activation
    // 
    function transfer (int256[] memory activation) public view returns(int256[] memory){
        int256[] memory arr = new int256[](activation.length);
        for (uint i = 0; i < activation.length; i++){
            arr[i] = PRBMathSD59x18.div(one, (one + PRBMathSD59x18.exp(-activation[i])));
        }

       return arr;
    }

    
    // def transfer(activation):
    // 	return 1.0 / (1.0 + exp(-activation))

    // # Forward propagate input to a network output
    //  int256[][][] memory network, int256[] memory row
    // [[[1,2,3],[1,2,3]],[[1,2,3],[1,2,3]]],[1,2,3] for test
    function forward_propagate (int256[][][] memory network, int256[] memory row) public view returns(int256[] memory, int256[][] memory){
        int256[] memory inputs = row;
        int256[][] memory neuron_output = new int256[][](network.length);  //store the outputs of neuron of each layer
        for (uint i = 0; i < network.length; i++){       
            for (uint j = 0; j < network[i].length; j++){
                int256[] memory activation = activate(network[i], inputs);
                neuron_output[i] = transfer(activation);
            }
            // set the new inputs as the neuron array
            for (uint k = 0; k < network[i].length; k++){
                inputs[k] = neuron_output[i][k];
            }      
        }
        return (inputs, neuron_output);
        
    }

    // def forward_propagate(network, row):
    // 	inputs = row
    // 	for layer in network:
    // 		new_inputs = []
    // 		for neuron in layer:
    // 			activation = activate(neuron['weights'], inputs)
    // 			neuron['output'] = transfer(activation)
    // 			new_inputs.append(neuron['output'])
    // 		inputs = new_inputs
    // 	return inputs

    // # Calculate the derivative of an neuron output
    function transfer_derivative (int256 output) public pure returns(int256){
        return PRBMathSD59x18.mul(output, (int256(1e18)- output));
    }

    // def transfer_derivative(output):
    // 	return output * (1.0 - output)

    // # Backpropagate error and store in neurons
    // need more checking for this function, mainly about the representation of the network i.e. weights, output and delta.
    // expected.length must be equal to neuron_output
    // [[[1,2,3],[1,2,3]],[[1,2,3],[1,2,3]]],[0,1],[[1,2],[1,2]]
    function backward_propagate_error (int256[][][] memory network, int256[] memory expected, int256[][] memory neuron_output) public view returns(int256[][] memory){
        int256[][] memory neuron_delta = new int256[][](network.length);

        for (uint i = network.length; i > 0; i--){   // because solidity does not support >= so, we start with network.length instead of network.length - 1 
            int256[][] memory layer = network[i-1];
            int256[] memory errors = new int256[](layer.length) ;  
            int256[] memory delta = new int256[](layer.length);   
            
            if (i != network.length ){
               for (uint j = 0; j < layer.length; j++){ 
                   int256 error = int256(0);
                   for (uint k = 0; k < network[i-1].length; k++){ 
                       error = error + PRBMathSD59x18.mul ( network[i-1][k][j], delta[k] );
                   }
                   errors[j] = error;
               }
            }
            else {
               for (uint j = 0; j < layer.length; j++){ 
                   errors[j] = neuron_output[i-1][j]- expected[j];
               } 
            }
            for (uint j = 0; j < layer.length; j++){ 
                delta[j] = PRBMathSD59x18.mul ( errors[j], transfer_derivative(neuron_output[i-1][j]));
            }
            neuron_delta[i-1] = delta; 
        }
        return neuron_delta;
        
    }
    // def backward_propagate_error(network, expected):
    // 	for i in reversed(range(len(network))):
    // 		layer = network[i]
    // 		errors = list()
    // 		if i != len(network)-1:
    // 			for j in range(len(layer)):
    // 				error = 0.0
    // 				for neuron in network[i + 1]:
    // 					error += (neuron['weights'][j] * neuron['delta'])
    // 				errors.append(error)
    // 		else:
    // 			for j in range(len(layer)):
    // 				neuron = layer[j]
    // 				errors.append(neuron['output'] - expected[j])
    // 		for j in range(len(layer)):
    // 			neuron = layer[j]
    // 			neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

    // # Update network weights with error
    // note that the row does not contain the labels 
    //  [[[1,2,3],[1,2,3]],[[1,2,3],[1,2,3]]],[1,2,3],[1],[[1,2],[1,2]],[[1,2],[1,2]]
    function update_weights (int256[][][] memory network, int256[] memory row, int256 l_rate, int256[][] memory neuron_output, 
                             int256[][] memory neuron_delta) public view returns(int256[] memory) {
        for (uint i = 0; i < network.length; i++){
            int256[] memory inputs = new int256[](row.length);
            //copy the values of row except the last one (i.e. the label) to inputs, since we assume that row does not contain labels when can need not to use row.length-1 here
            for (uint l = 0; l < row.length; l++){
                inputs[l] = row[l];
            }
            if (i !=0){
                for (uint l = 0; l < neuron_output[i-1].length; l++){   // the output from the (i-1)-th layer (do not include the input layer)
                    inputs = neuron_output[l];
                }
            }
            for (uint j = 0; j < network[i].length; j++){ 
                for (uint k = 0; k <  network[i][j].length; k++){ // neuron weights here are network[i][j]  i.e. neuron_weights[k] =  network[i][j][k] 
                    network[i][j][k]  = network[i][j][k]  - PRBMathSD59x18.mul (PRBMathSD59x18.mul ( l_rate, neuron_delta[i][j]), network[i][j][k]);
                    //PRBMathSD59x18.mul(l_rate, neuron_delta[i][j]);
                }
                // network[i][j][network[i][j].length] = network[i][j][network[i][j].length] - PRBMathSD59x18.mul(l_rate, neuron_delta[j][network[i][j].length]);
            }
        }
        
    }
    // def update_weights(network, row, l_rate):
    // 	for i in range(len(network)):
    // 		inputs = row[:-1]
    // 		if i != 0:
    // 			inputs = [neuron['output'] for neuron in network[i - 1]]
    // 		for neuron in network[i]:
    // 			for j in range(len(inputs)):
    // 				neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]
    // 			neuron['weights'][-1] -= l_rate * neuron['delta']

    // # Train a network for a fixed number of epochs
    // expected.length must be equal to n_outputs
    //  [[[1,2,3],[1,2,3]],[[1,2,3],[1,2,3]]],[[1,2,3]],[1,2],[1],[1],[2]
    function train_network (int256[][][] memory network, int256[][] memory train,  uint[] memory label, int256 l_rate, uint n_epoch, uint n_outputs) public view returns(int256[][][] memory) {
        
        for (uint i = 0; i < n_epoch; i++){
            int256 sum_error = 0;
            int256[][] memory neuron_output;
            int256[][] memory neuron_delta;
            int256[] memory expected = new int256[](n_outputs);
            int256[] memory outputs;
            for  (uint j = 0; j < train.length; j++){
                (outputs, neuron_output)  = forward_propagate(network, train[j]);
                // initialize all the values in expected as 0
                for  (uint k = 0; k < n_outputs; k++){
                    expected[k] = 0;
                }
                // use 0/1 classification to indicate the label of a row. e.g. [0,0,1,0,0] means its label is actually 2 if the n_ouputs are [0,1,2,3,4].
                // however the data type int256 for train prevents us from getting the real label and setting it as 1, so we seperate train into train and label as the arguments
                expected[label[j]] = 1e18;
                for  (uint m = 0; m < expected.length; m++){
                    sum_error = sum_error + PRBMathSD59x18.mul ( (expected[m]-outputs[m]),  (expected[m]-outputs[m]) );
                }
                neuron_delta = backward_propagate_error(network, expected, neuron_output);
                // // return neuron_output, neuron_weights, neuron_delta ... TBC
                update_weights(network, train[j], l_rate, neuron_output, neuron_delta);

            }
            
        }
        return network;
    }

 

    function predict (int256[][][] memory network, int256[][] memory row) public {
        for (uint p = 0; p < row.length; p++){
            int256[] memory inputs = row[p];
            int256[][] memory neuron_output = new int256[][](network.length);  //store the outputs of neuron of each layer
            for (uint i = 0; i < network.length; i++){       
                for (uint j = 0; j < network[i].length; j++){
                    int256[] memory activation = activate(network[i], inputs);
                    neuron_output[i] = transfer(activation);
                }
                // set the new inputs as the neuron array
                for (uint k = 0; k < network[i].length; k++){
                    inputs[k] = neuron_output[i][k];
                }      
            }
        }
        // return (inputs, neuron_output);
        
    }
  
        
          


}