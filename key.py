from random import random

TARGET_PRIME_LENGTH = 10

## (a ** b ) % m
##      ==
## (a * a * ... * a) % m
##  ^ b times     ^
##      ==
## ( ( (a ** k) % m ) * (a ** (b - k) ) ) % m  
##  for a ** k >= m and k <= b

##
#  Miller-Rabin Prime Test
##

## TODO: Later on we will implement a random a picker
def give_a(n):
	return 70

## TODO: Add length modifier to n
def give_start_n():
	return int(random() * 10 ** (TARGET_PRIME_LENGTH))

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


if __name__ == '__main__':
	print("Testing")
	n = give_start_n()
	s, d = give_s_d(n)
	print ("n", n, d * 2 ** s, n - d * (2 ** s))
	print ("s", s)
	print ("d", d)
	print ("is prime", is_prime(n))
	for k in range(100):
		p = is_prime(n + k)
		if p:
			print(n + k, "is prime")
