const Banking = artifacts.require("Banking")

contract('Banking', (accounts) => {
  let banking;

  before(async () => {
    banking = await Banking.deployed();
  });

  describe("Testing banking", async () => {
    
    it("Assert no owners on any accounts", async () => {
        const owners = await banking.getAccountOwners()
        owners.forEach(uint => {
            assert.equal(uint, 0, "ID of develop account # 0")
        });
    });
    it("Assert owner of account#0 is now sender", async () => {
        await banking.setAccountOwner(0)
        const owner = await banking.getAccountOwner(0)
        assert.equal(owner, accounts[0], "ID of develop account # 0")
    });
    it("Assert deposits go through", async () => {
        await banking.deposit(0,1000)
        const balance = await banking.getBalance(0)
        assert.equal(balance, 1000, "Balance should be 1000")
    });
    it("Assert transfer of money", async () => {
        await banking.transfer(1,0,500)
        const bal1 = await banking.getBalance(0)
        const bal2 = await banking.getBalance(0)
        assert.equal(bal1, 500, "Balance should be 500")
        assert.equal(bal2, 500, "Balance should be 500")
    });
    it("Assert withdrawal of money", async () => {
        await banking.withdraw(0,450)
        const bal1 = await banking.getBalance(0)
        assert.equal(bal1, 50, "Balance should be 0")
    });
    it("Assert withdrawal of more money isn't possible", async () => {
        const result = await banking.withdraw(0,100)
        const bal1 = await banking.getBalance(0)
        assert.equal(bal1, 50, "Balance should be 0")
    });

  });
});
