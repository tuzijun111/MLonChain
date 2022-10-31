#include <iostream>
#include <vector>
#include <cmath>
using namespace std;


int euclidean_distance(vector<int> row1, vector<int> row2){
    int distance = 0;
    for (int i = 0; i < row1.size(); i++){
        distance = distance + pow((row1[i]-row2[i]), 2);
    }
    return distance;
}

int main() {
    cout << "\n";
    int n_feature = 10;
    int n_input = 100;
    vector<vector<int> > train(n_input, vector<int>(n_feature, 1));
    vector<int> test(n_feature, 2);
    vector<int> distances(n_input);

    for (int i = 0; i < n_input; i++){
        distances[i] = euclidean_distance(train[i], test);
    }
    
    cout << distances[0];
    
}