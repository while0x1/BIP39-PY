# BIP39-PY
Generate BIP-0039 Words and Number Lists

Using just inbuilt python libraries you can generate BIP-0039 seed phrases.
In order to add a touch more security to your seed phrase backups instead of writing the words in plain-text - you can write the number location within the https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt worldist.
This utility facilitates the creation of the number list from an existing seed, restores a seed from a input number list, or can generate a new seed and number list. 

It is recommended to only use this tool on a completely air-gapped device. 

This tool relies on the randomness provided by random.SystemRandom().randbytes(16). 
