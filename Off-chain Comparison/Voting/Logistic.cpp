#include <iostream>
#include <vector>
using namespace std;


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

int main() {
    cout << "\n";
    int n_feature = 10;
    int n_input = 10000;
    vector<vector<int> > train(n_input, vector<int>(n_feature, 1));
    vector<vector<int> > test(1, vector<int>(n_feature, 2));
    int l_rate = 1;
    int n_epoch = 1;
    vector<int> res = logistic_regression(train, test, l_rate, n_epoch);
    cout << res[0];
    
}