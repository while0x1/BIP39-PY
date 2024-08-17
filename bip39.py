import os
import random
import hashlib
import sys
from pycardano import HDWallet, PaymentVerificationKey, Network, Address

with open('bip39_words.txt','r') as f:
    wordList = f.read().splitlines()

print('Enter Option:')
print(' 1 - Generate a new Seedphrase')
print(' 2 - Calculate seed numbers from existing seed')
print(' 3 - Restore seed from existing seed numbers')
print(' 4 - Derive Cardano Address from a Seedphrase')

state = input()

#Generate New Phrase
if state == '1':
    print('Enter Option:')
    print(' 1 - 12 Words')
    print(' 2 - 24 Words')
    seedlen = input()    
    
    if seedlen == '1':
        entropy = random.SystemRandom().randbytes(16)
    elif seedlen == '2':
        entropy = random.SystemRandom().randbytes(32)
    else:
        print('invalid option')
        sys.exit()
    checksum = hashlib.sha256(entropy).digest()
    seedbytes_hex = entropy.hex() + checksum.hex()[0]
    seedbits = bin(int(seedbytes_hex , base=16))[2:]
    bitlist = list(map(''.join, zip(*[iter(seedbits)]*11)))
    seedphrase = []
    seednumbers = []

    for bits in bitlist:
        num = int(bits, 2)
        seedphrase.append(wordList[num])
        seednumbers.append(str(num))
        
    print(f'Generated seedphrase - {" ".join(seedphrase)}')
    print('')
    print(f'Seed numbers {" ".join(seednumbers)}')
#Calculate seed numbers
elif state == '2':
    try:
        print('Paste seed to generate numeric sequence')
        seedIn = input()

        seed = seedIn.split(' ')
        numlist = []
        for word in seed:
            cnt = 0
            for bip in wordList:
                if word == bip:
                    numlist.append(cnt)
                    break   
                cnt += 1
        print(f' Seed numbers: {numlist}')
    except Exception as e:
        print(e)
        print('Encountered error - pasted seed correctly?')
#Restore seed from number list
elif state == '3':
    try:
        print('Paste number list to generate seed')
        numsin = input()
        numlist = numsin.split(' ')
        rseed = []
        for n in numlist:
            rseed.append(wordList[int(n.strip())])
        print(f'Seed phrase: {" ".join(rseed)}')
    except Exception as e:
        print(e)
        print('Encountered error - paste numbers in correct format?')

elif state == '4':
    try:
        print('Paste seed to derive address')
        seedIn = input()
        hdwallet = HDWallet.from_mnemonic(seedIn)
        hdwallet_stake = hdwallet.derive_from_path("m/1852'/1815'/0'/2/0")
        stake_public_key = hdwallet_stake.public_key
        stake_vk = PaymentVerificationKey.from_primitive(stake_public_key)
        hdwallet_spend = hdwallet.derive_from_path("m/1852'/1815'/0'/0/0")
        spend_public_key = hdwallet_spend.public_key
        spend_vk = PaymentVerificationKey.from_primitive(spend_public_key)
        print(Address(spend_vk.hash(), stake_vk.hash(), network=Network.MAINNET).encode())

    except Exception as e:
        print(e)
        print('Error Encountered - seed pasted correctly?')

