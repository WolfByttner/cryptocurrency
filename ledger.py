#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from math import log10, floor
from ipaddress import IPv6Address
from functools import reduce

##
#  Utility Variables
##

hasher = hashlib.sha224
z_len = 5

AddressType = IPv6Address

##
#  End Utility Variables
##

##
#  Utility Functions
##

def isfloat(num):
	try:
		float(num)
		return True
	except Exception:
		return False
##
#  End Utility Functions
##

class Coin:
	magn = 12

	def _getval(self, val):
		if type(val) == int:
			v = val * 10 ** self.magn
		elif type(val) == float or (type(val) == str and isfloat(val)):
			spl = str(val).split(".")
			if spl[0].startswith('-'):
				sign = -1
				spl[0] = spl[0].lstrip('-')
			else:
				sign = 1
			if len(spl[0]) > 0:
				v = self._getval(int(spl[0]))
			else:
				v = 0
			if len(spl) > 1 and len(spl[1]) > 0:
				v += reduce(lambda x, y: x * 10 + y,
						[int(i) for i in 
							spl[1].ljust(self.magn, '0')[0:self.magn]])
			v *= sign
		elif type(val) == Coin:
			v = val.value
		else:
			raise TypeError("Type has not been defined")
		return v

	def __init__(self, value, _raw = False):
		if _raw and type(value) == int:
			self.value = value
		else:
			self.value = self._getval(value)

	def __repr__(self):
		s = ""
		if (self.value < 0):
			s += '-'
		value = abs(self.value)
		if value >= 10 ** self.magn:
			s += str(int(value / 10 ** self.magn)) + '.'
		else:
			s += '0.'
		if value % (10 ** self.magn) != 0:
			s += '0' * (self.magn - (int(floor(log10(
					value % (10 ** self.magn))) + 1)))
			s += str(value % (10 ** self.magn)).rstrip('0')
		return s
	
	def __str__(self):
		return "£" + self.__repr__()

	def __iadd__(self, other):
		self.value += self._getval(other)
		return self

	def __isub__(self, other):
		self.value += self._getval(other)
		return self

	def __add__(self, other):
		return Coin(self.value + self._getval(other), _raw = True)

	def __sub__(self, other):
		return Coin(self.value - self._getval(other), _raw = True)
	
	## TODO: Redefine this
	#def __mul__(self, integ):
	#	if type(integ) == Coin:
	#		return Coin(self.value * integ.value)
	#	return Coin(self.value * integ)
	
	@classmethod
	def one(self):
		return Coin(1)
	
	@classmethod
	def frac(self):
		return Coin(1, _raw = True)


class Address(AddressType):
	def __init__(self, address):
		super(Address, self).__init__(address)


class Transaction:

	def validate_addr(self, address, name):
		if type(address) == Address:
			return (address)
		elif type(address) == AddressType:
			return (Address(str(AddressType)))
		else:
			raise ValueError("{0} is not a valid address".format(name))
	
	def validate_amount(self, amount):
		if type(amount) == Coin:
			return amount
		elif type(amount) == int:
			return Coin(amoun)

	def __init__(self, addr_src, addr_target, amount):
		self.addr_src = self.validate_addr(addr_src, "Source")
		self.addr_target = self.validate_addr(addr_target, "Target")
		self.amount = amount
	
	def __repr__(self):
		s = "{0} sends {1} to {2}".format(
			self.addr_src, self.amount, self.addr_target)
		return s

	# Takes a string and returns a transaction
	#@classmethod
	#def transcribe(cls, string):
	#	return


class Entry:
	def __init__(self, head = None, transactions = [], hashnums = []):
		self.head = head ## Hexadecimal, unique in the ledger
		self.transactions = transactions
		self.hashnums = hashnums
	
	def validate(self):
		valid = True
		if len(self.transactions) != 50:
			valid = False
		elif len(self.hashnums) != 5:
			valid = False
		for i in range(len(self.hashnums)):
			t = "\n".join(map(str, transactions[i*10:(i + 1)*10]))
			if not hasher(t + str(self.hashnums[i]).encode('utf-32')).hexdigit().startswith('0'*z_len):
				valid = False
				break;
		return valid


