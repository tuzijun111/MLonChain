#include <iostream>
#include <vector>
#include <cmath>
#include <tuple>

//#include <stdarg.h>
//#include <stdio.h>      /* vsnprintf */

#include "encalve1.h"
#include "encalve1_t.h"  /* print_string */

using namespace std;
/* 
 * printf: 
 *   Invokes OCALL to display the enclave buffer to the terminal.
 */
/*
void printf(const char *fmt, ...)
{
    char buf[BUFSIZ] = {'\0'};
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(buf, BUFSIZ, fmt, ap);
    va_end(ap);
    ocall_encalve1_sample(buf);
}*/


int predict(vector<int> row, vector<int> coefficients) {
    int yhat =  coefficients[coefficients.size()-1];
    for (int i=0; i < coefficients.size()-1; i++) {
        yhat = yhat + coefficients[i] * row[i];
    }
    return yhat;
}

vector<int> coefficients_sgd(vector<vector<int> > train, int l_rate, int n_epoch){
    vector<int> coef(train[0].size());
    for (int i=0; i < train[0].size(); i++) {
        coef[i] = 0;
    }
    for (int i=0; i < n_epoch; i++) {
        for (int j=0; j < train.size(); j++) {
            int yhat = predict(train[j], coef);
            int error = train[j][train[0].size()-1] - yhat;
            for (int m=0; m < (train[0].size()-1); m++) {
                // coef[m] = 1;
                coef[m] = coef[m] + (l_rate*error) * yhat * train[j][m];
            }
        }
    }
    return coef;
}

vector<int> logistic_regression(vector< vector<int> > train, vector<vector<int> > test, int l_rate, int n_epoch){
    vector<int> prediction(test.size());
    vector<int> coef = coefficients_sgd(train, l_rate, n_epoch);
    for (int i = 0; i<test.size(); i++){
        int yhat = predict(test[i], coef);
        if (yhat > 5){
            prediction[i] = 1;
        }
        else{
            prediction[i] = 0;
        }
    }
    return prediction;
}

int LR() {
    int n_feature = 10;
    int n_input = 60000;
    vector<vector<int> > train(n_input, vector<int>(n_feature, 1));
    vector<vector<int> > test(1, vector<int>(n_feature, 2));
    int l_rate = 1;
    int n_epoch = 10;

    vector<int> res = logistic_regression(train, test, l_rate, n_epoch);
    return 0;
}

int euclidean_distance(vector<int> row1, vector<int> row2){
    int distance = 0;
    for (int i = 0; i < row1.size(); i++){
        distance = distance + pow((row1[i]-row2[i]), 2);
    }
    return distance;
}

int knn() {
    int n_feature = 10;
    int n_input = 100000;
    vector<vector<int> > train(n_input, vector<int>(n_feature, 1));
    vector<int> test(n_feature, 2);
    vector<int> distances(n_input);

    for (int i = 0; i < n_input; i++){
        distances[i] = euclidean_distance(train[i], test);
    }
    return 0;
}

vector<int> activate(vector< vector<int> > weights, vector<int> input) {
    vector<int> activation(weights.size());
    for (int i=0; i < weights.size(); i++) {
        for (int j = 0; j < weights[0].size(); j++){
            activation[i] = activation[i] + weights[i][j]*input[j];
        }
    }
    return activation;
}

vector<int> transfer(vector<int> activation){
    vector<int> arr(activation.size());
    for (int i =0; i<activation.size(); i++){
        arr[i] = 1/(1+activation[i]);
    }
    return arr;
}

// typedef struct{
//     double max, min;
// } number_range;

// vector<vector <int> >
std::tuple<vector<int>, vector<vector <int> > > forward_propagate(vector<vector <vector <int> > > network, vector<int> row)
// -> std::tuple<vector<int>, vector<vector <int> > >
{
    vector<int> inputs = row;
    vector<vector <int> > neuron_output(network.size(), vector<int>(network[0].size(), 0));
    for (int i =0; i<network.size(); i++){
        for (int j =0; j<network[0].size(); j++){
            // vector<int> activation(network[i].size(), 1);
            vector<int> activation = activate(network[i], inputs);
            neuron_output[i] = activation;
            // neuron_output[i] = transfer(activation);
        }
        for (int k =0; k<network[0].size(); k++){
            inputs[k] = neuron_output[i][k];
        }
    }
    // struct result {vector<int> in; vector<vector <int> > neu;};
    // return result {inputs, neuron_output};
    return {inputs, neuron_output};
}

int transfer_derivative(int output){
    return output*(pow(10, 18)-output);
}

vector<vector <int> > backward_propagate_error(vector<vector <vector <int> > > network, vector<int> expected, vector< vector<int> > neuron_output){
    vector<vector <int> > neuron_delta(network.size(), vector<int>(network[0].size(), 0));
    vector<int> errors(network[0].size(), 0);
    vector<int> delta(network[0].size(), 0);
    for (int i = 0; i<network.size(); i++){
        for (int j = 0; j<network[0].size(); j++){
            errors[j] = neuron_output[i][j] - expected[j];
        }
        for (int j = 0; j<network[0].size(); j++){
            // delta[j] = 10;
            // delta[j] = errors[j] * neuron_output[i][j];
            delta[j] = errors[j] * transfer_derivative(neuron_output[i][j]);
        }
        neuron_delta[i] = delta;
    }
    return neuron_delta;
}

vector<vector <vector <int> > > update_weights(vector<vector <vector <int> > > network, vector<int> row, int l_rate,
vector<int> neuron_output, vector< vector <int> > neuron_delta){
    for (int i = 0; i<network.size(); i++){
        vector<int> inputs = row;
        for (int j = 0; j<network[0].size(); j++){
            for (int k = 0; k<network[0][0].size(); k++){
                network[i][j][k] = network[i][j][k] - l_rate*neuron_delta[i][j]*network[i][j][k];
            }
        }
    }
    return network;
}

vector<vector <vector <int> > > train_network(vector<vector <vector <int> > > network, vector<vector <int> > train,
vector<int> label, int l_rate, int n_epoch, int n_outputs){

    for (int i = 0; i<n_epoch; i++){
        int sum_error = 0;
        for (int j = 0; j<train.size(); j++){
            vector <int> outputs(network[0].size());
            vector<vector <int> > neuron_output(network[0].size(), vector<int>(network.size(), 0));
            tie(outputs, neuron_output) = forward_propagate(network, train[j]);
            // i.e. the vector that should be returned from forward_propagate() function, since two vectors can not
            // be returned, we simulate the computation as follows:

            // vector<int> outputs(network[0].size(), 1);
            vector<int> expected(n_outputs);
            for (int k = 0; k<network[0].size(); k++){
                sum_error = sum_error + (expected[k] - outputs[k]*(expected[k] - outputs[k]));
            }
            vector< vector<int> > neuron_delta = backward_propagate_error(network, expected, neuron_output);
        }
    }
    return network;
}



void NN() {
    int n_layer = 3;
    int n_feature = 2;
    int n_input = 2000;
    int n_outputs = 2;
    // vector< vector < vector<int> > > network(n_layer, vector< vector<int> >(n_feature, vector<int>(n_outputs, 1)));
    // vector<vector<int> > train(4, vector<int>(n_feature, 2));
    // vector<int> label(n_feature, 1);
    vector< vector < vector<int> > > network = {{{0,0}, {0,0}}, {{0,0}, {0,0}}, {{0,0}, {0,0}}};

    vector<vector<int> > train (n_input,vector<int>(n_feature, 1));

    vector<int> label = {0,0,1,0};

    int l_rate = 1;
    int n_epoch = 50;

    vector <int> outputs(network[0].size());
    vector<vector <int> > neuron_output(network[0].size(), vector<int>(network.size(), 0));

    tie(outputs, neuron_output) = forward_propagate(network, train[0]);


    // int p1 = 2;
    // int p2 = 1;

    // int p = 1/(2+pow(10, 18));



    vector< vector < vector <int> > > res = train_network(network, train, label, l_rate, n_epoch, n_outputs);

    // for (auto v: res){
    //     for (auto ele: v){
    //         cout << ele << " ";
    //     }
    //     cout << endl;
    // }

    // for (int i = 0; i < train.size(); i++){
    //     for (int j = 0; j < train[i].size(); j++)
    //     {
    //         cout << train[i][j] << " ";
    //     }
    //     cout << endl;
    // }
}

int ecall_encalve1_sample(int a[])
{
	//printf("%d", a[0]);
 //NN();
 for(int i = 0;i < 2000000000; i++){
   	int b = 1;
   }
  return 0;
}

