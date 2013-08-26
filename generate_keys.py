from Crypto.PublicKey import ElGamal
from Crypto import Random

import cPickle as Pickle

v_priv_key = ElGamal.generate(128, Random.new().read)
v_pub_key = v_priv_key.publickey()

s_priv_key = ElGamal.generate(128, Random.new().read)
s_pub_key = s_priv_key.publickey()

Pickle.dump(v_priv_key, open("vending_key.priv", 'w'))
Pickle.dump(v_pub_key, open("vending_key.pub", 'w'))
Pickle.dump(s_priv_key, open("server_key.priv", 'w'))
Pickle.dump(s_pub_key, open("server_key.pub", 'w'))