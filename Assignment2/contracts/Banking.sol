//SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.7.0;


contract Banking {
	
	address[10] public accounts;
	mapping(uint => int) public balance;

	//sets value of current account in accounts to sender
	function setAccountOwner(uint account) public {
		//Array is limited to 10 accounts
		require(account<=10&&account>=0);
		accounts[account] = msg.sender;
	}

	function deposit(uint account, int riches) public returns (bool) {
		if(account<=10&&account>=0) {
			balance[account]+= riches;
			return true;
		} else {
			return false;
		}
	} 

	function transfer(uint to, uint from, int riches) public returns (bool) {
		//I know, shut up.
		if(to<=10&&to>=0&&from<=10&&from>=0&&accounts[from]==msg.sender&&balance[from]>=riches) {
			balance[from]-= riches;
			balance[to]+= riches;
			return true;
		} 
			
		return false;
		
	}

	function withdraw(uint account, int riches) public returns (bool) {
		if(account<=10&&account>=0&&balance[account]>=riches&&accounts[account]==msg.sender) {
			balance[account]-= riches;
			return true;
		} else {
			return false;
		}
	}

	//Is view due to view only nature
	function getBalance(uint account) public view returns (int) {
		return balance[account];
	}

	//memory keyword to create temp space instead of using storage
	function getAccountOwners() public view returns (address[10] memory) {
		return accounts;
	}

	function getAccountOwner(uint account) public view returns (address) {
		return accounts[account];
	}
}