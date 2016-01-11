#!/usr/bin/python
# Encryption key = Owaspiitkchapter
# Text to be encrypted = padding oracle is way faster than brute-force
import base64
from Crypto.Cipher import AES
from Crypto import Random

def bin_to_str(bin_string):
	temp = bin_string.split(':')
	bin_string = ''
	for i in temp:
		bin_string += chr(int(i, 2))
	return bin_string

def str_to_bin(string):
	return ':'.join('{0:08b}'.format(ord(x), 'b') for x in string)

# PKSC17 Padding 

def pad(string):
	l = len(string)
	rem = 16 - l%16
	if(rem==0):
		rem = 16
	val = chr(rem)
	for i in range(rem):
		string += val
	return string

def unpad(string):
	val = string[-1]
	rem = ord(val)
	if rem>16 or rem<1:
		raise Exception('Padding is incorrect')
	for i in range(rem):
		if string[-1] == val:
			string = string[:-1]
		else:
			raise Exception('Padding is incorrect')
	return string

# AES Cipher class to encrypt, decrypt and padding validator
class padding_aes: 
	def __init__( self, key ):
		self.key = key

	def encrypt( self, raw ):
		raw = pad(raw)
		iv = Random.new().read( AES.block_size )
		cipher = AES.new( self.key, AES.MODE_CBC, iv )
		enc = (iv + cipher.encrypt(raw)) 
		return enc

	def decrypt( self, enc ):
		iv = enc[:16]
		cipher = AES.new(self.key, AES.MODE_CBC, iv )
		raw = unpad(cipher.decrypt( enc[16:] ))
		return raw		

	def padding( self, enc ):
		iv = enc[:16]
		cipher = AES.new(self.key, AES.MODE_CBC, iv )
		try:
			raw = cipher.decrypt( enc[16:] )
			actual = unpad(raw)
			return ord(raw[-1])
		except:
			return 0

def padding_oracle(ciphertext):
	cipher = padding_aes('Owaspiitkchapter')
	return cipher.padding(ciphertext)

# def padding_oracle(ciphertext):
# 	characters = ciphertext.split(':')
# 	ciphertext = ''
# 	for i in characters:
# 		ciphertext += chr(int(i, 2))
# 	cipher = padding_aes('Owaspiitkchapter')
# 	return cipher.padding(ciphertext)

if __name__ == '__main__':
	ciph = AESCipher('Owaspiitkchapter')
	ci = ciph.encrypt('padding oracle is way faster than brute-force')
	pl = ciph.decrypt(ci)
	print ':'.join('{0:08b}'.format(ord(x), 'b') for x in ci)
	# print ci, pl 