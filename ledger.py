import hashlib
from math import log10, ceil

##
#  Utility Variables
##

hasher = hashlib.sha224
z_len = 5

##
#  End Utility Variables
##

class Coin:
	def __init__(self, value):
		self.value = value ## TODO: Store as int 
	
	def __repr__(self):
		s = ""
		if self.value >= 10 ** 12:
			s += str(int(self.value / 10 ** 12)) + '.'
		else:
			s += '0.'
		if self.value % 10 ** 12 != 0:
			s += '0' * (12 - (int(ceil(log10(self.value % 10 ** 12)))))
			s += str(self.value % (10 ** 12)).rstrip('0')
		return s




class Transaction:
	def __init__(self, addr_src, addr_target, amount):
		self.addr_src = addr_src
		self.addr_target = addr_target
		self.amount = amount
	
	def __repr__(self):
		s = "{1} sends {2} to {3}".format(
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


