zokrates compile -i test.zok
zokrates setup
zokrates compute-witness -a argument1 argument2 ...       
// grep '~out' witness   (to show the return value)
zokrates generate-proof
zokrates export-verifier
zokrates verify




export PATH=$PATH:/Users/binbingu/.zokrates/bin







# compile
zokrates compile -i root.zok
# perform the setup phase
zokrates setup
# execute the program
zokrates compute-witness -a 337 113569
# generate a proof of computation
zokrates generate-proof
# export a solidity verifier
zokrates export-verifier
# or verify natively
zokrates verify





