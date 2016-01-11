#!/usr/bin/python
from oracle import padding_oracle
from oracle import bin_to_str
from oracle import str_to_bin

def increment_byte(string, index):
	string = list(string)
	string[index] = chr((ord(string[index])+1)%256)
	return ''.join(string)

def set_byte(string, istate, val):	
	string = list(string)
	start = 15-val+2
	for i in range(start, 16):
		string[i] = chr(val^istate[i])
	return ''.join(string)

c1_original = '00000010:10011010:11101010:00101001:11100011:01011001:00110011:01101111:10010001:00100000:11001101:00101101:11001001:10000110:11001011:10100100'
c1_new = '00100010:10010010:10101010:10101100:00100011:01011001:01010011:01101001:10000101:00101100:11110101:00101101:10110001:11100000:10001111:10111100'
p2 = ''
c2_original = '11111011:10000110:01001110:11111101:00100010:01001010:11000000:10100100:01001110:01001001:00101001:01100111:10111001:10010100:10111111:01101011'

c1_original = bin_to_str(c1_original)
c2_original = bin_to_str(c2_original)
c1_new = bin_to_str(c1_new)
istate = [0]*16

# Caculating last bit of intermediate state
for i in range(256):
	c1_new = increment_byte(c1_new, 15)
	# print ord(c1_new[15])
	code = padding_oracle(c1_new + c2_original)
	if code>0:
		istate[15] = code^ord(c1_new[15])
		print istate[15]

for j in range(14, -1, -1):
	val = 16-j
	for i in range(j+1, 16):
		c1_new = set_byte(c1_new, istate, val)
	for i in range(256):
		c1_new = increment_byte(c1_new, j)
		# print ord(c1_new[15])
		code = padding_oracle(c1_new + c2_original)
		if code>0:
			istate[j] = code^ord(c1_new[j])
			print istate[j]

print istate
# print c1_original
# temp = c1_original.split(':')
# randomst = ''
# for i in temp:
# 	randomst+= chr(int(i, 2))
# print randomst
# c1_original = bin_to_str(c1_original)
c1_original = list(c1_original)
a = []
for i in range(16):
	a.append(chr(ord(c1_original[i])^istate[i]))
print ''.join(a)