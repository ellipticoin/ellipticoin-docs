## Deploying a Smart Contract
A smart contract is a piece of code that runs on a blockchain. Once deployed to a blockchain the code cannot be changed and execution of the code can’t be cancelled. Even the person who deployed it can’t cancel execution or change the code.

One of the most popular use-cases for a smart contracts is to create crypto tokens. Crypto tokens can be used from anything from raising money in a crowd sale to [representing hamburgers](https://www.cnbc.com/2017/08/28/burger-king-russia-cryptocurrency-whoppercoin.html)    

This guide will show you how to build and deploy your own token to the Ellipticoin testnet. To make things more interesting we'll make our coin have a special property: every time you spend it the recipient will get twice as many coins as you sent. Obviously this currency won’t be very useful, but hey, the fed can print money and people still trust them so why can't we!

## Setup
First you’ll need to install the nightly version of the [Rust](https://www.rust-lang.org/) programming language if you haven’t already:

    $ curl -sSf https://sh.rustup.rs | sh
    $ rustup toolchain install nightly

You'll also need the WebAssembly target

    $ rustup target add wasm32-unknown-unknown --toolchain nightly

Finally you'll need the `ec` Cargo plugin which is used for creating smart contracts on Ellipticoin.

    $ cargo install cargo-ec

## Creating a project
Now that we have our toolchain set up let's create our project:

    $ cargo ec new doubler_coin && cd doubler_coin

`cargo-ec` will create a token contract by default to get you started.

## Testing
Next let's run the tests and make sure they pass

    
    $ cargo test
    ...
    test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out


Success!

Now let's update our test. Every time someone sends some tokens the recipient should receive twice as many. Update line 57 to reflect that

    assert_eq!(get_balance(&bob()), 40);

And run our test. It should fail with the following message:

    $ cargo test
    ...
    thread 'doubler_coin::tests::test_transfer' panicked at 'assertion failed: `(left == right)`
    left: `20`,
    right: `40`', src/doubler_coin.rs:57:9
    ...
    test result: FAILED. 2 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out

Now lets update our code. Change line 19 to the following to double the amount of tokens the recipient will receive.

    set_balance(&to, get_balance(&to) + amount * 2);

Run the tests again and they should pass!

## Compilation
Next you'll need to compile to WebAssembly:

    cargo ec build

This will create the following file: `target/wasm32-unknown-unknown/release/doubler_coin.wasm`



## Deployment
Now we're ready to deploy our token to the Ellipticoin testnet!


To do that we'll need to install and initialize the Ellipticoin wallet

    $ npm install -g ec-wallet
    $ ec-wallet init

Next ask for some Ellipticoins in the Ellipticoin chat.

Now you're ready to deploy! Run the following to do so:

    $ ec-wallet deploy target/wasm32-unknown-unknown/release/doubler_coin-min.wasm doubler_coin 150000

`150000` is passed as an argument to the constructor which will issue the deployer (you) that many tokens specified in thousandths.

Wait 5 seconds or so for your transaction to be mined and check your balance!

## Running Your Smart Contract
First lets check that deployment worked by checking our balance

Run the following replacing the Ellipticoin address with your own:

    $ ec-wallet balance vQMn3JvS3ATITteQ+gOYfuVSn2buuAH+4e8NY/CvtwA=:doubler_coin vQMn3JvS3ATITteQ+gOYfuVSn2buuAH+4e8NY/CvtwA=
    100.00

The first argument is the contract identifier. Contract identifiers are made up of the public key that deployed the contract concatenated with the contract's name. The second augment is the address to get the balance of.

Now let's transfer some tokens! (replacing the Ellipticoin address with your own again)

    $ ec-wallet transfer vQMn3JvS3ATITteQ+gOYfuVSn2buuAH+4e8NY/CvtwA=:doubler_coin PQjxd4sLn+QsGPCwqwCCYUEYYh01OT9LFNn/vwkA4Xw= 1
    Transferred 1 vQMn3JvS3ATITteQ+gOYfuVSn2buuAH+4e8NY/CvtwA=:doubler_coin to PQjxd4sLn+QsGPCwqwCCYUEYYh01OT9LFNn/vwkA4Xw=

Looks like it worked!

Let's check the balances of our account and the account we sent tokens to to make sure:

    ec-wallet balance vQMn3JvS3ATITteQ+gOYfuVSn2buuAH+4e8NY/CvtwA=:doubler_coin PQjxd4sLn+QsGPCwqwCCYUEYYh01OT9LFNn/vwkA4Xw=
    99.0000
    ec-wallet balance vQMn3JvS3ATITteQ+gOYfuVSn2buuAH+4e8NY/CvtwA=:doubler_coin vQMn3JvS3ATITteQ+gOYfuVSn2buuAH+4e8NY/CvtwA=
    2.00

🎉 it worked!

Thanks for following along. If you have any questions or suggestions on how to make Ellipticoin better please stop by the [Ellipticoin Telegram room](https://t.me/ellipticoin) and say hello!

