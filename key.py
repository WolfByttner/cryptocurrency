from random import random, randint
from math import sqrt

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

def get_message_int(message):
	return reduce(lambda x, y: int(x) * 256 + int(y), map(ord, message))

##
#  Traditional RSA algorithm
#  As seen on: https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29
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


if __name__ == '__main__':
	e, d, n = get_RSA_key_pair()
	#m = get_message_int("Hello World!")
	m = 3456789
	c = pow(m, e, n)
	print(m == pow(c, d, n))

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
