#===============================================================================
# from Crypto.PublicKey import RSA
# from Crypto import Random
#===============================================================================

from ezPyCrypto import key

while 1:
#def generate_key():
	my_key = key(320)
	
	priv_key = my_key.exportKeyPrivate()
	pub_key = my_key.exportKey()
	
	key_file = open("server_key_ez.priv", "w")
	key_file.write(priv_key)
	key_file.close()
	
	key_file = open("server_key_ez.pub", "w")
	key_file.write(pub_key)
	key_file.close()
	break
#===============================================================================
# 	random_generator = Random.new().read
# 
# 	private_key = RSA.generate(1024, random_generator)
# 	public_key = private_key.publickey()
# 	
# 	key_file = open("server_key.priv", "w")
# 	key_file.write(private_key.exportKey())
# 	key_file.close()
# 	
# 	key_file2 = open("server_key.pub", "w")
# 	key_file2.write(public_key.exportKey())
# 	key_file2.close()
#===============================================================================