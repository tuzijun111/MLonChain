const API_KEY = "WIYEPYWikXeubjVSB1lnQB9RaZBa5oNP"
const PUBLIC_KEY = "0x4f165218486CAE53022802701882b52d108076C3"
const PRIVATE_KEY = "7865c3bdd68113e704cea5a8fb002fda782005ab1a4680a7fbae31f01d320eb3"
const API_URL = "https://goerli.infura.io/v3/88e080f6cca34d0895a6a8f7fe1c00a6";


const CONTRACT_ADDRESS = "0x587096F52927dC1F71FA3EF0a445907485731F6B"  //Prediction.zok


// Infura provider
// var url = 'https://ropsten.infura.io/v3/88e080f6cca34d0895a6a8f7fe1c00a6'
const Web3 = require('web3');
const web3 = new Web3(
    new Web3.providers.HttpProvider(API_URL)
    );

const contract = require('/Users/binbingu/Documents/Codes/JavaScript/JS/Verifier.json');
// web3.eth.defaultAccount = PRIVATE_KEY;




async function main() {
    let verifier = new web3.eth.Contract(contract.abi, CONTRACT_ADDRESS);
    const proof = require('/Users/binbingu/Documents/Codes/JavaScript/JS/proof.json'); 
    // console.log(jsonData);
    //console.log(proof.proof);
    let cost = await verifier.methods.verifyTx(proof.proof, proof.inputs).estimateGas();
    // let a = 1;
    
    // let b = 2;
   
    // let cost = await verifier.methods.verifyTx(a, b).call();
    console.log("The fee is: " + cost);
    
}


main();