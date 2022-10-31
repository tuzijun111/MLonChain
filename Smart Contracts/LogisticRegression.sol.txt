// SPDX-License-Identifier: Unlicense
pragma solidity >=0.8.4;

import "https://github.com/tuzijun111/Solidity-Library/blob/main/math-contract/PRBMathSD59x18.sol";



contract LogisticRegression {
    using PRBMathSD59x18 for int256;
    int256 one = 1e18;
    int256 half = 5e17;
    
     
    //dataset  
    // int256[] x1 = [int256(1_000000000000000000), int256(2_000000000000000000), int256(4_000000000000000000), int256(3_000000000000000000), int256(0)];
    // int256[] x2 = [int256(1_000000000000000000), int256(2_000000000000000000), int256(4_000000000000000000), int256(3_000000000000000000), int256(0)];
    // int256[] x3 = [int256(1_000000000000000000), int256(2_000000000000000000), int256(4_000000000000000000), int256(3_000000000000000000), int256(0)];
    // int256[] x4 = [int256(2_000000000000000000), int256(2_000000000000000000), int256(5_000000000000000000), int256(2_000000000000000000), int256(1_000000000000000000)];
    // int256[] x5 = [int256(3_000000000000000000), int256(2_000000000000000000), int256(4_000000000000000000), int256(3_000000000000000000), int256(1_000000000000000000)];
  
    // //int256[][] inputdata = [x1, x2, x3, x4, x5];
    // int256[][] train_data = [x1, x2, x3, x4, x5, x6, x7, x8];
    // int256[][] test_data = [x9, x10];
    // int256 learning_rate = 1e17; //i.e. 0.1
    // uint num_epoch = 5;

    // training: test = 4:1
    
    constructor() public{
        //push more values to each x
        // for (uint i = 0; i < 15; i++) {   
        //     x1.push(int256(1_000000000000000000));
        // }
        // for (uint i = 0; i < 15; i++) {   
        //     x2.push(int256(1_000000000000000000));
        // }
        // for (uint i = 0; i < 15; i++) {   
        //     x3.push(int256(1_000000000000000000));
        // }
        // for (uint i = 0; i < 15; i++) {   
        //     x4.push(int256(1_000000000000000000));
        // }

        
        // //push more values to inputdata
        // for (uint i = 0; i < 15; i++) {
        //     train_data.push(x1);
        // }
        // for (uint i = 0; i < 3; i++) {
        //     test_data.push(x4);
        // }
        
    }
    
      
    // Find the min and max values for each column
    // function dataset_minmax() public view returns(uint256){   //int256[2] memory
    //     int256[2][] memory minmax;  //minmax[0]=min   []minmax[1] =max
    //     // for (uint i =0; i < inputdata[0].length; i++){

    //     // }
    //     return inputdata.length;   //rows
    //     // for i in range(len(dataset[0])):
    //     //     col_values = [row[i] for row in dataset]
    //     //     value_min = min(col_values)
    //     //     value_max = max(col_values)
    //     //     minmax.append([value_min, value_max])
    //     // return minmax
    // }


    // Linear Regression Algorithm With Stochastic Gradient Descent
    function logistic_regression(int256[][] memory train, int256[][] memory test, int256 l_rate, uint256 n_epoch) public view returns(int256 [] memory){
        int256 [] memory prediction = new int256[](test.length);
        uint num_coef = train[0].length;
        int256 [] memory coef;
        coef = coefficients_sgd(train, l_rate, n_epoch);
        for (uint i =0; i < test.length; i++){
            int256 yhat = predict(test[i], coef);
            if (yhat>=half){         //i.e. >=0.5, round to 1
                prediction[i] = 1;
            }
            else{
                prediction[i] = 0;
            }
        }
        return prediction;
    }
        // predictions = list()
        // coef = coefficients_sgd(train, l_rate, n_epoch)
        // for row in test:
        //     yhat = predict(row, coef)
        //     yhat = round(yhat)
        //     predictions.append(yhat)
        // return(predictions)

    //Estimate logistic regression coefficients using stochastic gradient descent
    function coefficients_sgd(int256[][] memory train, int256 l_rate, uint256 n_epoch) public view returns(int256[] memory){
        uint num_coef = train[0].length;
        int256 [] memory coef = new int256[] (num_coef);
        for (uint i =0; i < train[0].length; i++){
            coef[i] = 0;
        }

        for (uint i =0; i < n_epoch; i++){
            for (uint j =0; j < train.length; j++){    // number of rows
                int256 yhat = predict(train[j], coef);
                int256 error = train[j][train[j].length-1] - yhat;  //i.e. the label (the last column of row) of a data x 
                for (uint m =0; m < train[j].length - 1; m++){
                    coef[m + 1] = coef[m + 1] + PRBMathSD59x18.mul(PRBMathSD59x18.mul(PRBMathSD59x18.mul  
                                    (PRBMathSD59x18.mul(l_rate, error), yhat), (one - yhat)), train[j][m]);

                }
            }
        }
        return coef;

        // coef = [0.0 for i in range(len(train[0]))]
        // for epoch in range(n_epoch):
        //     for row in train:
        //         yhat = predict(row, coef)
        //         error = row[-1] - yhat
        //         coef[0] = coef[0] + l_rate * error * yhat * (1.0 - yhat)
        //         for i in range(len(row)-1):
        //             coef[i + 1] = coef[i + 1] + l_rate * error * yhat * (1.0 - yhat) * row[i]
        // return coef
    }


        // Incremental training for big dataset
    function incremental_coefficients_sgd(int256[][] memory train, int256 l_rate, uint256 n_epoch, int256[] memory coef) public view returns(int256[] memory){
        // uint num_coef = train[0].length;
        // int256 [] memory coef = new int256[] (num_coef);
        // for (uint i =0; i < train[0].length; i++){
        //     coef[i] = 0;
        // }

        for (uint i =0; i < n_epoch; i++){
            for (uint j =0; j < train.length; j++){    // number of rows
                int256 yhat = predict(train[j], coef);
                int256 error = train[j][train[j].length-1] - yhat;  //i.e. the label (the last column of row) of a data x 
                for (uint m =0; m < train[j].length - 1; m++){
                    coef[m + 1] = coef[m + 1] + PRBMathSD59x18.mul(PRBMathSD59x18.mul(PRBMathSD59x18.mul  
                                    (PRBMathSD59x18.mul(l_rate, error), yhat), (one - yhat)), train[j][m]);

                }
            }
        }
        return coef;
    }

    function predict(int256[] memory row, int256[] memory coefficients) public view returns(int256){
        int256 yhat = coefficients[0];
        for (uint j =0; j < (row.length-1); j++){
            yhat += PRBMathSD59x18.mul(coefficients[j+1], row[j]);
        }   
        return PRBMathSD59x18.div(one, (one + PRBMathSD59x18.exp(-yhat)));
    }

    function predict2(int256[][] memory row, int256[] memory coefficients) public{
        int256 yhat = coefficients[0];
        for (uint i =0; i < row.length; i++){
            for (uint j =0; j < row[0].length; j++){
                yhat += PRBMathSD59x18.mul(coefficients[j+1], row[i][j]);
            }   
        }
        // return PRBMathSD59x18.div(one, (one + PRBMathSD59x18.exp(-yhat)));
    }


    




    


}