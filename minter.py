#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ledger import Entry, hasher, z_len

class Minter:
	def __init__(self, ledger_reader, ledger = None):
		if ledger != None:
			self.reader = ledge_reader(ledger)
		else:
			self.reader = ledger_reader
	
	def mint(self, entry):
		ledger_head = self.reader.get_head()

