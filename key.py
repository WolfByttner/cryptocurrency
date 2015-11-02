from random import random, randint
from math import sqrt
from functools import reduce, partial
import hashlib

## More than 20 and Python struggles
TARGET_PRIME_LENGTH = 15 

## (a ** b ) % m
##      ==
## (a * a * ... * a) % m
##  ^ b times     ^
##      ==
## ( ( (a ** k) % m ) * (a ** (b - k) ) ) % m  
##  for a ** k >= m and k <= b

def extended_gcd(a, b):
	r0 = a
	r1 = b
	s0 = 1
	s1 = 0
	t0 = 0
	t1 = 1
	while (r1):
		q = r0 / r1
		r0, r1 = r1, r0 - q * r1
		s0, s1 = s1, s0 - q * s1
		t0, t1 = t1, t0 - q * t1

def inverse_mod(a, n):
	t0 = 0
	t1 = 1
	r0 = n
	r1 = a
	while (r1):
		q = int(r0 / r1)
		t0, t1 = t1, t0 - q * t1
		r0, r1 = r1, r0 - q * r1
	if r0 > 1:
		return False ## A is not invertible
	if t0 < 0:
		t0 = t0 + n
	return t0

##
#  Miller-Rabin Prime Test
##

## TODO: Later on we will implement a random a picker
def give_a(n):
	return 70

## TODO: Add length modifier to n
def give_start_n():
	return int(random() * 10 ** (TARGET_PRIME_LENGTH - 1)) * 6 + 1
	#return (10 ** 8) * 6 + 1

def give_s_d(n):
	b = 2 ## For speed
	s = 1
	while not (n / b) % 2:
		b *= 2
		s += 1
	d = int(n / b)
	return s, d

def is_prime(n, k = 0):
	a = give_a(n)
	s, d = give_s_d(n)
	x = pow(a, d, n) ## Modular Exponentiation
	if not (x == 1 or x + 1) == n:
		for r in range(s):
			x = pow(x, 2, n)
			if not (x == 1 or x + 1 == n):
				return False
	return True

def find_prime(n = None):
	if n == None:
		n = give_start_n()
	s, d = give_s_d(n)
	for attempt in range(0, 120000, 6):
		if is_prime(n + attempt):
			return n + attempt
	return find_prime()

##
#  These are not padded and are quite easy to break with a plaintext attack
#  Going to implement a padding scheme later
#  https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding
##
def get_int_from_message(message):
	return reduce(lambda x, y: int(x) * 256 + int(y), map(ord, message))
## TODO: Handle utf-8 (and other encodings)
def get_message_from_int(i):
	s = ""
	while (i):
		c = i % 256
		s += chr(c)
		i -= c
		i //= 256 ## integer division
	return s[::-1]



##
#  Traditional RSA algorithm
#  As seen at: https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29
##
def get_RSA_key_pair():
	p = find_prime()
	q = find_prime()
	n = p * q
	## from Φ(n) = Φ(p)Φ(q) = (p ** k - p ** (k - 1))...
	## = (p ** 1 - p ** 0)(q ** ... 
	## = p * q - p - q + 1
	Φn = n - (p + q - 1)
	e = find_prime(randint(50000, 300000))
	d = inverse_mod(e, Φn) ## TODO: Check for failure
	return e, d, n

##
#  These functions are here for reference and use with Partial
##

## These functions in particular can be changed to convert the message
## to an int with a different padding structure
RSA_mtoi = get_int_from_message
RSA_itom = get_message_from_int

## e is the Public Key
## d is the Private Key
def RSA_encrypt(n, e, message, plaintext = True):
	if plaintext:
		message = RSA_mtoi(message)
	return pow(message, e, n)

def RSA_decrypt(n, d, encrypted_message, plaintext = True):
	message =  pow(encrypted_message, d, n)
	if plaintext:
		message = RSA_itom(message)
	return message
		

def RSA_sign(n, d, message, hasher = hashlib.md5, encoding = 'utf-8'):
	hash_value = int(hasher.md5(message.encode(encoding)), 16)
	return RSA_decrypt(n, d, hash_value, False)

def RSA_verify(n, e, encrypted_message, message,
			hasher = hashlib.md5, encoding = 'utf-8'):
	hash_value = int(hash.md5(message.encode(encoding)), 16)
	return hash_value == RSA_encrypt(n, e, encrypted_message, False)

if __name__ == '__main__':
	e, d, n = get_RSA_key_pair()
	#m = get_message_int("Hello World!")
	m = 3456789
	c = pow(m, e, n)
	print(m == pow(c, d, n))
	message = "Hello World!"
	key_length = n
	public_key = e
	private_key = d
	m = RSA_encrypt(key_length, public_key, message)
	print(m, str(RSA_decrypt(key_length, private_key, m)))
	#print(find_prime())
	#print("Testing")
	#n = give_start_n()
	#s, d = give_s_d(n)
	#print ("n", n, d * 2 ** s, n - d * (2 ** s))
	#print ("s", s)
	#print ("d", d)
	#print ("is prime", is_prime(n))
	#for tries in range(0, 120000, 6):
	#	p = is_prime(n + tries)
	#	if p:
	#		print(n + tries, "is prime")
	#		break;
