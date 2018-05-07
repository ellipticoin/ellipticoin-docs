# Ellipticoin Documentation

Welcome to the Ellipticoin documentation! Ellipticoin is still in early
development so these pages may change frequently. If you notice
anything that could be improved please [make a PR](https://github.com/ellipticoin/ellipticoin-docs)!

## Getting Started

Ellipticoin standard tokens are equivalent to ERC20 tokens in Ethereum ecosystem. They can be used from anything from raising money in a crowd sale to [representing hamburgers](https://www.cnbc.com/2017/08/28/burger-king-russia-cryptocurrency-whoppercoin.html). This guide will show you how to build and deploy your own token to the Ellipticoin testnet. To make things more interesting we'll make our coin have a special property: every time you spend it the recipient will get twice as many coins as you sent. Obviously this currency won’t be very useful. But hey, the fed can print money and still remain relevant so why can’t we!

First you’ll need to install the ellipicoin wallet `ec-wallet`:

    npm install ec-wallet

Next, let’s initialize two accounts:

    $ ec-wallet init
    Initialization done. Your elipticoin address is choose-oblige-172
    $ ec-wallet init
    Initialization done. Your elipticoin address is critic-agree-829

This will create public and private keys and configure your wallet to use them when signing transactions.

We’ll use the first account for testing purposes. Copy down this address for later.

After we’ve initialized our wallet we’re ready to generate our smart contract code:

    ec-wallet new doubler_coin

First let's open up `doubler_coin/src/doubler_coin.rs` and see what an Elliptiocoin
token contract looks like.

    #[cfg(not(test))]
    use alloc::vec::Vec;
    use error::{self, Error};

    use ellipticoin::*;

    pub struct DoublerCoin<T: BlockChain>  {
        pub blockchain: T
    }

    impl <B> DoublerCoin<B> where B: BlockChain {
        pub fn constructor(&self, initial_supply: u64) {
            self.write(self.sender(), initial_supply);
        }

        pub fn balance_of(&self, address: Vec<u8>) -> u64 {
            self.read(&address)
        }

        pub fn transfer(&self, receiver_address: Vec<u8>, amount: u64)  -> Result<(), Error> {
            let sender_balance = self.read(&self.sender());
            let receiver_balance = self.read(&receiver_address);

            if sender_balance > amount {
                self.write(self.sender(), sender_balance - amount);
                self.write(receiver_address, receiver_balance + amount);
                Ok(())
            } else {
                Err(error::INSUFFIENT_FUNDS)
            }
        }

        fn sender(&self) -> Vec<u8> {
            self.blockchain.sender()
        }

        fn read(&self, key: &Vec<u8>) -> u64 {
            self.blockchain.read_u64(key.to_vec())
        }

        fn write(&self, key: Vec<u8>, value: u64) {
            self.blockchain.write_u64(key, value)
        }
    }

The first few lines import the different libraries necessary to interface with
the Ellipticoin blockchain. Then we define the `DoublerCoin` struct which has
one element `blockchain` which we will use to read and write to the blockcain.

We also define 3 public methods:

`constuctor` is method that is automatically called when a smart contract is
deployed. In our constructor we mint some amount of tokens to the `sender` which will be
whoever deployed the contract.

`balance_of` reads the balance from the contract state. Each contract has it's
own key-value store of bytes similar to how [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) works for websites.

`transfer` first checks the sender's balance. If the sender has enough funds it
will subtract them from the sender's account and add them to the receiver's account. If not it will return an error.

Now let’s build our code and run the tests

    npm install && npm build && npm test

You should see the following output:

    > doubler-coin@0.1.0 test /Users/masonf/src/ec-wallet/doubler_coin
    > cargo build --target wasm32-unknown-unknown --release --lib &&       mocha test

    Finished release [optimized] target(s) in 0.29 secs


    DoublerCoin
     constructor
       ✓ should initalize the sender with 100 tokens
     balance_of
       ✓ should return your balance
       ✓ should return 0 for unknown addresses
     transfer
       ✓ decreases the senders balance by the amount specified
       ✓ increases the receivers balance by the amount specified
       ✓ returns an error if you try to send more tokens than you have


    6 passing (167ms)


Note the contract code is written in Rust but the integration tests are written in Javascript. Theoretically you could write your integration tests in Rust as well but I found writing integration tests in Javascript more enjoyable. There’s also an example unit test at `src/doubler_coin_test.rs`.

Next let’s add our custom functionality. Since we’re good developers well update the test file first.

open up `test/doubler-coin-test.js`

and change line `60` from

    it('increases the receivers balance by the amount specified', async function() {

to

    it('increases the receivers balance by twice the amount specified', async function() {

and change line `66` from

    assert.equal(result, 20);

to

    assert.equal(result, 40);

and run the tests again:

    npm test


You should get the following result:

     > doubler-coin@0.1.0 test /Users/masonf/src/ec-wallet/doubler_coin
     > cargo build --target wasm32-unknown-unknown --release --lib &&      mocha test

      Finished release [optimized] target(s) in 0.25 secs


    DoublerCoin
       constructor
       ✓ should initalize the sender with 100 tokens
     balance_of
       ✓ should return your balance
       ✓ should return 0 for unknown addresses
     transfer
       ✓ decreases the senders balance by the amount specified
       1) increases the receivers balance by the amount specified
       ✓ returns an error if you try to send more tokens than you have


    5 passing (145ms)
    1 failing

    1) DoublerCoin transfer increases the receivers balance by the amount specified:

       AssertionError [ERR_ASSERTION]: 20 == 40
       + expected - actual

       -20
       +40

       at Context.<anonymous> (test/doubler-coin-test.js:66:14)
       at <anonymous>



    npm ERR! Test failed.  See above for more details.


Now let’s make the change to our code.

open up `src/doubler_coin.rs`

and change line 26 from:

    self.write(receiver_address, receiver_balance + amount);

to

    self.write(receiver_address, receiver_balance + amount * 2);

Let’s run our tests again and they should now pass!

    DoublerCoin
     constructor
       ✓ should initalize the sender with 100 tokens
     balance_of
       ✓ should return your balance
       ✓ should return 0 for unknown addresses
     transfer
       ✓ decreases the senders balance by the amount specified
       ✓ increases the receivers balance by the amount specified
       ✓ returns an error if you try to send more tokens than you have


    6 passing (176ms)

Now that we have our coin working the way we want to can deploy it to the Ellipticoin testnet!

    npm run  deploy -- 100

we added the `--` so we could [pass arguments through to the deployment command](https://docs.npmjs.com/cli/run-script#description). This argument is an to the constructor which specifies how many tokens to “mint” when creating the contract.

We can now call methods against our token contract!

First let’s get our balance:


    $ ec-wallet get critic-agree-829 DoublerCoin balance_of critic-agree-829
    critic-agree-829/DoublerCoin.balance_of(critic-agree-829)
    => 100

This is correct: the contract minted 100 tokens to the deploying account as specified in the previous step. Now let’s make a transaction and check that out contract logic works as expected (note: here’s is where you’ll use the address you created at the beginning of the guide):


    $ ec-wallet post critic-agree-829 DoublerCoin transfer choose-oblige-172 7
    $ ec-wallet get critic-agree-829 DoublerCoin balance_of critic-agree-829 critic-agree-829/DoublerCoin.balance_of(critic-agree-829)
    => 93
    $ ec-wallet get critic-agree-829 DoublerCoin balance_of choose-oblige-172 critic-agree-829/DoublerCoin.balance_of(choose-oblige-172)
    => 14


It worked! We sent 7 tokens and the recipient received 14! 🎉

If you're interested in hearing more about Ellipticoin and staying up to date on our roadmap head over to the [Telegram room](https://t.me/joinchat/F0_SEksYp5PhexXW6dQ-9A) and say hi!
