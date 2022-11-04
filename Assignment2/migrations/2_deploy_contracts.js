const Banking = artifacts.require("Banking");

module.exports = function(deployer) {
  deployer.deploy(Banking);
};
