import requests
import json
import random

#Fixed URL and headers for the server.
url = "http://dennis:test@192.168.0.118:8332"
headers = {'content-type': 'application/json'}

#annoying random wallet name requirement due to wallet naming issues in Docker. 
#This is just because I don't want to delete all the wallet data every time I run this.
wallet1name = "wallet"+ str(random.randint(1,10000))
wallet2name = "wallet"+ str(random.randint(1,10000))

#payloads for doing certain things with descriptive names
LISTWALLETS = { "jsonrpc": "1.0", "id": "PythonRCP", "method": "listwallets", "params": [] }
CREATEFIRSTWALLET = {"jsonrpc": "1.0", "id": "PythonRCP", "method": "createwallet", "params": [wallet1name]}
CREATESECONDWALLET = {"jsonrpc": "1.0", "id": "PythonRCP", "method": "createwallet", "params": [wallet2name]}


#Defines a standard POST request and returns the response
def postRequest(payload, URL):
    response = requests.post(
        URL, data=json.dumps(payload), headers=headers).json()
    return(response)


def main():

    #Quickly running through the process of generating 2 wallets, 2 addresses, 50 bitcoins of the first 101 blocks mined and then transferring 25 of them to the second address.
    #I did get lazy about halfway through so the code sucks. Good luck reading it.

    print(postRequest(LISTWALLETS, url))
    print(postRequest(CREATEFIRSTWALLET, url))

    #The wallet RPC call requires the URL to change, not the parameter, so quick fix:
    #I also need the walletadress to send coins around later.
    wallet1address = postRequest({"jsonrpc": "1.0", "id": "PythonRCP", "method": "getnewaddress", "params": []}, url+"/wallet/"+wallet1name)["result"]
    print(wallet1address)
    
    #Shotgunning it once again:
    print(postRequest(CREATESECONDWALLET, url))
    wallet2address = postRequest({"jsonrpc": "1.0", "id": "PythonRCP", "method": "getnewaddress", "params": []}, url+"/wallet/"+wallet2name)["result"]
    print(wallet2address)

    #Listing available wallets to prove they have been created
    print(postRequest(LISTWALLETS, url))

    #generating 101 bitcoin (at least 101 are required since the first 100 aren't going to be verified, and will be listed as "untrusted".)
    #This is of course a dev only RPC call, and isn't listed in the RPC cheatsheet, annoyingly.
    print(postRequest({"jsonrpc": "1.0", "id": "PythonRCP", "method": "generatetoaddress", "params": [101, wallet1address]}, url))
    
    print("------------------------------------------------------------------------------------------------------")
    
    #Checking balances of our two wallets. Should show 50 bitcoins ready to spend.
    print(postRequest({"jsonrpc": "1.0", "id": "curltest", "method": "getbalances", "params": []},url+"/wallet/"+wallet1name))
    print(postRequest({"jsonrpc": "1.0", "id": "curltest", "method": "getbalances", "params": []},url+"/wallet/"+wallet2name))
    
    #Transfer 25 coins to the address of wallet 2, with no other parameters, so we will use the fallback fee of 0.0001
    print(postRequest({"method": "sendtoaddress", "params": [wallet2address, 25]},url+"/wallet/"+wallet1name))
   
    #check balances again. Will show the 25 coins on the second wallet as "untrusted" for the same reason as mentioned above.
    print(postRequest({"jsonrpc": "1.0", "id": "curltest", "method": "getbalances", "params": []},url+"/wallet/"+wallet1name))
    print(postRequest({"jsonrpc": "1.0", "id": "curltest", "method": "getbalances", "params": []},url+"/wallet/"+wallet2name))


if __name__ == "__main__":
    main()