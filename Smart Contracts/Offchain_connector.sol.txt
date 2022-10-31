// SPDX-License-Identifier: Unlicense
pragma solidity >=0.8.0;


contract Offchain {
   
    string request;
    event Request(string from, string request);
    uint256[] model;
    uint256[][] network;

    function update(string memory from, string memory request, uint256[] memory m) public returns(uint256[] memory){
        model = m;
        emit Request(from, request);
        return model;     
    }
    // update neural network
    function twod_update(string memory from, string memory request, uint256[][] memory m) public returns(uint256[][] memory){
        network = m;
        emit Request(from, request);
        return network;     
    }

    // function testcase(int256 a, int256 b) public view returns (int256) {
    //     int256 c = a + b;
    //     return c;

    // }

    function sim_compute(uint256[][] memory m) public {
        for (uint i = 0; i < m.length; i++){
            for (uint j = i+1; j < m.length; j++){
                for (uint k = 0; k < m[0].length; k++){
                    if (m[i][k] != m[j][k]){
                        break;
                    }
                } 
            }                    
        }
    }
}


