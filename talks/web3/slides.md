## Smartcontract Exploitation

Martin

---

### Overview

 * Big Picture: Blockchains and Smartcontracts
 * The target: EVM & Solidity
 * The court: Blockchains in CTFs
 * The tools: metamask, remix, hardhat

---

### Blockchain

 * Distributed system with shared state
 * Idea: "Money is Memory"
 * Distribution of coins as a list of transactions
     * State can be verified
     * "Just" need to agree on the transactions
 * Blocks: chunk of new transactions
 * Keypairs as accounts

----

### Blockchain: Consensus

 * Works as long as everyone has same transaction list
 * Who gets to extend the Blockchain?
 * Consensus: Proof-of-Work, Proof-of-Stake, Proof-of-X
 * Irrelevant for CTFs

----

### Blockchain: Visual

![](https://c.m5w.de/uploads/65dd4895-47b7-4b90-91c2-a93afebbb177.png)

----

### Smartcontracts

 * Focus on Ethereum / EVM
 * Extend the idea: store and modify arbitrary state instead of balances
 * New type of users: programs
 * Like transfers: need to be deterministic
     * Run by every node to compute state update

----

### Smartcontracts: Transactions

 * Send bytecode & create new contract
    * Executes contact constructor to init state
 * Call method on new contract
     * Contract address is target. Call options as txdata
     * State can be updated
 * Invalid contract call
     * Contract code triggers revert

---

### Solidity

 * Lanuage used in the ethereum ecosystem
     * object-oriented, high-level language for implementing smart contracts
     * influenced by C++, Python and JavaScript
     * statically typed, supports inheritance, libraries and complex user-defined types
 * Compiles to EVM bytecode
     * Non-ethereum EVM chains exist
 * Smartcontracts can use other languages (or handcraft EVM bytecode)

----

### Solidity: Hello World

```solidity
pragma solidity ^0.8.17;

contract Counter {
    uint public count;

    function get() public view returns (uint) {
        return count;
    }

    function inc(uint amount) public {
        count += amount;
    }

    function dec() public {
        // This function will fail if count = 0
        count -= 1;
    }
}
```

----

### Solidity: Tokens

```solidity
pragma solidity ^0.8.17;

contract Counter {
    mapping(address => uint) public balance;

    constructor() {
        balance[msg.sender] = 1000 ether;
    }

    // Function to increment count by 1
    function transfer(address recv, uint amount) public {
        require(balance[msg.sender] >= amount);
        balance[msg.sender] -= amount;
        balance[recv] += amount
    }
}
```

----

### Solidity: Modifiers

```solidity
modifier onlyOwner() {
    require(msg.sender == owner, "plz leave");
    _;
}

function printMoney() public onlyOnwer {
    // ...
}
```

----

### Solidity: Calls & transfers

```solidity
pragma solidity ^0.8.17;

contract Example {
    Token token;

    constructor() {
        token = new Token();
    }

    function cashout() public {
        token.transfer(msg.sender, 1 ether) // contract call
        msg.sender.call{value: 1 ether}("") // native
    }
}
```

----

### Solidity: Reentrancy

```solidity
pragma solidity ^0.8.17;

contract Example {
    mapping(address => uint256) balance;
    
    function cashout(uint256 amount) public {
        require (balance[msg.sender] > amount, "no");
        msg.sender.call{value: amount}("");
        balance[msg.sender] -= amount;
    }
}

contract Attack {
    Example e;
    
    attack(Example _e) {
        e = _e;
        e.cashout(1 ether);
    }
    
    fallback() external payable {
        e.cashout(1 ether);
    }
}
```

----

### Solidity: Delegate call

```solidity
contract A {
    uint test = 0;
    
    function c(address b) public {
        b.delegatecall(
            abi.encodeWithSignature("stuff()")
        );
    }
}

contract B {
    uint test = 0; // same as A
    
    function stuff() public {
        // lots of code, expensive to store
        test = 1337; // A.test = 1337
    }
}
```

----

### Solidity: "randomness"

```solidity
contract Vuln {
    function random() public payable returns (uint256) {
        return uint256(blockhash(block.number-1));
    }
}
```

----

### Solidity: Interfaces

 * ERC: standards & interfaces for smartcontracts
     * ERC20 popular interface for tokens
     * ERC721 interface for NFTs
 * FOSS implementations exists and can be used

----

### Solidity: Real world token

```solidity
pragma solidity ^0.8.17;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.0.0/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor(string memory name, string memory symbol)
    
    ERC20(name, symbol) {
        // Mint 100 tokens to msg.sender
        // Similar to how
        // 1 dollar = 100 cents
        // 1 token = 1 * (10 ** decimals)
        _mint(msg.sender, 100 * 10 ** uint(decimals()));
    }
}
```

----

### Solidity: ???

 * https://solidity-by-example.org/
 * https://learnxinyminutes.com/docs/solidity/
 * https://docs.soliditylang.org

---

### Blockchains in CTFs

 * Transactions cost money: using real chains is expensive
 * Proof-of-Work costs energy: wastefull
 * Most CTFs run single node Proof-of-authority chains
 * Blockchain clients provide client & developer APIs
     * Only thing that we are interested in

----

### Blockchains in CTFs
 * Sometimes public testnets are used
     * Transactions are public: solves are public
 * Faucets are provided to get coins for free
 * Sometimes remote provisions contract instance for every player

----

### Tools to use

 * Metamask: wallet, manage accounts
 * Remix: browser based solidity IDE
 * web3.js / web3\.py: RPC client libs
 * hardhat: web3 development framework

----

### Tools: Metamask

 * Browser extension
 * Can create multiple accounts / keys
 * Can export keys
 * Talks to mainnet node by default, supports custom RPCs

----

### Tools: Remix

 * IDE + Debug environment
 * Usefull to write "exploit contracts"
 * EVM environment in the browser
 * Can use "injected metamask" provider to talk to custom chains

----

### Tools: web3.* & hardhat

 * Usefull for more advanced exploits
 * Provide lots of dev tooling

---

### Challenges

 * Intro chals from Slack
 * KITCTFCTF ethereum challenge
 * https://ethernaut.openzeppelin.com/
 * https://www.damnvulnerabledefi.xyz/
     * Focus on inter-contract vulns
