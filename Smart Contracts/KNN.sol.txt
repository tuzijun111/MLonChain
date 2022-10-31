// SPDX-License-Identifier: Unlicense
pragma solidity >=0.8.4;

import "https://github.com/tuzijun111/Solidity-Library/blob/main/math-contract/PRBMathSD59x18.sol";
//import "https://github.com/tuzijun111/Solidity-Library/blob/main/math-contract/PRBMath.sol";



contract KNN {
    using PRBMathSD59x18 for int256;
    // using PRBMath for uint256;
    int256 one = 1e18;
    int256 half = 5e17;

    // int256[] row1 = [int256(1_000000000000000000), int256(1_000000000000000000)];
    // int256[] row2 = [int256(3_000000000000000000), int256(3_000000000000000000)];
    // int256[] row3 = [int256(2_000000000000000000), int256(2_000000000000000000)];
    // int256[] row4 = [int256(9_000000000000000000), int256(9_000000000000000000)];

    // int256[][] train = [row1, row2, row3, row4];
    // int256[] testrow =  [int256(2_000000000000000000), int256(1_000000000000000000)];
    // uint256 num_neighbors = 3;
    
     

    //  the Euclidean distance between two vectors
    
    function euclidean_distance (int256[] memory row1, int256[] memory row2) public view returns(int256){
        int256 distance = 0;
        for (uint i = 0; i < row1.length; i++){
            distance = distance + ((row1[i]-row2[i])*(row1[i]-row2[i])/one);
        }
        //return distance;
        return PRBMathSD59x18.sqrt(distance);
    }


    // Locate the most similar neighbors for a single data item 
    function get_neighbors (int256[][] memory train, int256[][] memory test, uint256 num_neighbors) public view returns(uint256[][] memory ){
        uint256[][] memory neighbors = new uint256[][](num_neighbors);
        // note that testrow must be uint256 in order to support "push" operator for arrays
        for (uint p = 0; p < test.length; p++){ 
            uint256[] memory distances = new uint256[](train.length);
            for (uint i = 0; i < train.length; i++){          
                int256 dist = euclidean_distance(test[p], train[i]);
                distances[i] = uint256(dist);       
            }
            //Currently only find the smallest value since using quicksort algorithm will change the state of the variable "distances"
            // Will use a naive way to find top smallest values here
            //return MinEle(distances);
            
            for(uint256 j = 0; j < num_neighbors; j++){
                neighbors[j] = SortTopN(distances, j);
            }
        }         
            
        return neighbors;
            //return distances;
    }

    //KNN_prediction() need to know all the data 
    function KNN_prediction (int256[][] memory data, int256[] memory testdata, uint256 num_neighbors) public view returns(uint256[] memory ){

    }



    function MinEle(uint256[] memory arr) public pure returns(uint256, uint256){
        uint256 smallest = 1e40; 
        uint256 k;
        for(uint256 i = 0; i < arr.length; i++){
            if(arr[i] < smallest) {
                smallest = arr[i]; 
                k = i;
            } 
        }
        return (smallest, k);
    }

    function SortTopN(uint256[] memory arr, uint start) public pure returns(uint256[] memory){
        uint256 inter;
        uint256 k;
        for(uint256 i = start+1; i < arr.length; i++){
            //exchange arr[0] with the smallest value
            if(arr[i] < arr[start]) {
                inter = arr[start];
                arr[start] = arr[i];
                arr[i] = inter;
                k = i;
            } 
            else{
                inter = arr[start];
                k = start;
            }
        }
        uint256[] memory index = new uint256[](2);
        index[0] = inter;
        index[1] = k;

        return index;
    }

    // function quickSort(uint256[] memory arr, int left, int right) public {
    //     int i = left;
    //     int j = right;
    //     // if (i == j) return;
    //     uint pivot = arr[uint(left + (right - left) / 2)];
    //     while (i <= j) {
    //         while (arr[uint(i)] < pivot) i++;
    //         while (pivot < arr[uint(j)]) j--;
    //         if (i <= j) {
    //             (arr[uint(i)], arr[uint(j)]) = (arr[uint(j)], arr[uint(i)]);
    //             i++;
    //             j--;
    //         }
    //     }
    //     if (left < j)
    //         quickSort(arr, left, j);
    //     if (i < right)
    //         quickSort(arr, i, right);
       

    // }

    // function ConcatenateArrays(int256[] memory Accounts, int256[] memory Accounts2) public returns(int256[] memory) {
    //     int256[] memory returnArr = new int256[](Accounts.length + Accounts2.length);

    //     uint i=0;
    //     for (; i < Accounts.length; i++) {
    //         returnArr[i] = Accounts[i];
    //     }

    //     uint j=0;
    //     while (j < Accounts.length) {
    //         returnArr[i++] = Accounts2[j++];
    //     }

    //     return returnArr;
    // } 





    // function test1() public view returns(uint256[][] memory){
        
    //     return get_neighbors(train, testrow, num_neighbors);
    // }

 

    


}