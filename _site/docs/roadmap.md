Ellipticoin Consensus Mechanism Roadmap
=======================================

## 1. Proof of Work (complete)

Phase 1 of Ellipticoin runs Bitcoin's [nakamoto consensus
algorithm](https://bitcoin.org/bitcoin.pdf). The only difference is that the proof
of work function is
[hashfactor](https://gist.github.com/masonforest/e674ee749a01391f4ce7a35aa7bbf286)
instead of [hashcash](http://www.hashcash.org/).

## 2. Hybrid Proof of Work/Delayed Proof of Burn

Phase 2 of Ellipticoin will run a hybrid of proof of work and proof of burn
consensus algorithms. The proof of work algorithm will work the same as it did
in Phase 1. The proof of burn portion will allow miners to burn coins to give
them better chances of mining a block. This should have very similar incentives
as proof of work but instead of burning energy miners burn coins. This has a
couple major advantages. First, it's more environmentally friendly. Second, once
the coins are burned they can be recycled back into the issuance pool. This
means there will be more coins available to fund the security of the network.

It's possible to achieve this by requiring coins to be burned at the time of
mining but that could be taken advantage of. An attacker could use the coins won
in a previous block to mine the next block a so on which would have a
compounding effect. To prevent against this tokens are burned ahead of time and
a "maturity date" is set. The maturity date must be greater than two weeks in the
future. Therefore a miner would need to control 51% of the network for at least
two weeks to carry out the compounding attack described above.

## 3. Proof of Burn

The final Phase planned for Ellipticoin's consensus mechanism is a completely
Proof of Burn based algorithm. Miners will burn tokens as before but proof of
work mining will be removed. The winner of each block will be selected using the
[Signidice
algorithm](https://github.com/gluk256/misc/blob/master/rng4ethereum/signidice.md).
To bootstrap the network the final miner to win a block on the proof of work
chain will sign the proof of work value with an RSA key (ed25119 signatures
won't work in this case because they are non-determinaistic). This will produce
a 256 byte signature. This signature can then be used to select the next
winner using the  [follow the
satoshi](https://cardanodocs.com/cardano/proof-of-stake/#follow-the-satoshi)
algorithm. The next miner then signs that value which produces another random
value and so on. Miners will not be able to collect their reward unless they
sign the previous block. If the winning miner fails to mine a block a “second
place” miner will be selected and so on.
