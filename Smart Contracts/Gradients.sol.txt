// SPDX-License-Identifier: Unlicense
pragma solidity >=0.8.4;

import "https://github.com/tuzijun111/Solidity-Library/blob/main/math-contract/PRBMathSD59x18.sol";



contract Gradients {
    using PRBMathSD59x18 for int256;
    int256 one = 1e18;
    int256 half = 5e17;
    

  

    function predict(int256 x1, int256 x2, int256 theta_1, int256 theta_2) public returns(int256){
        int256 yhat = 0;  // i.e. theta_0 = 0
        yhat += x1*theta_1;
        yhat += x2*theta_2;
        return yhat;
        // yhat += PRBMathSD59x18.mul(x1, theta_1);
        // yhat += PRBMathSD59x18.mul(x2, theta_2); 
        // return PRBMathSD59x18.div(one, (one + PRBMathSD59x18.exp(-yhat)));
    }

    // we use the MSE (mean square error) loss function for gradients computation
    // assume that there are two features
    function gradient_mse(int256[][] memory train, int256[] memory label, int256 theta_1, int256 theta_2) public returns(int256, int256){
        int256[] memory x1 = new int256[](train.length);
        int256[] memory x2 = new int256[](train.length);
        int256[] memory y_pred = new int256[](train.length);
        int256 sum1 = 0;
        int256 sum2 = 0;
        for (uint i =0; i < train.length; i++){
            x1[i] = train[i][0];
            x2[i] = train[i][1];
            y_pred[i] = predict(x1[i], x2[i], theta_1, theta_2);
            sum1 = sum1 + (y_pred[i]-label[i])*x1[i];
            sum2 = sum2 + (y_pred[i]-label[i])*x2[i];
        }

        int256 n = int256(label.length); 
        
        int256 grad_1 = (2 / n) * sum1 ; 
        int256 grad_2 = (2 / n) * sum2 ; 
        return (grad_1, grad_2);

    }
}