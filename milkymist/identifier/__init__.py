from migen.fhdl.structure import *
from migen.bank.description import *
from migen.bank import csrgen

import re

def encode_version(version):
	match = re.match("(\d+)\.(\d+)(\.(\d+))?(rc(\d+))?", version, re.IGNORECASE)
	r = (int(match.group(1)) << 12) | (int(match.group(2)) << 8)
	subminor = match.group(4)
	rc = match.group(6)
	if subminor:
		r |= int(subminor) << 4
	if rc:
		r |= int(rc)
	return r

class Identifier:
	def __init__(self, address, sysid, version):
		self.sysid = sysid
		self.version = encode_version(version)
		
		self._r_sysid = RegisterField("sysid", 16, access_bus=READ_ONLY, access_dev=WRITE_ONLY)
		self._r_version = RegisterField("version", 16, access_bus=READ_ONLY, access_dev=WRITE_ONLY)
		self.bank = csrgen.Bank([self._r_sysid, self._r_version], address=address)
		
	def get_fragment(self):
		comb = [
			self._r_sysid.field.w.eq(self.sysid),
			self._r_version.field.w.eq(self.version)
		]
		return self.bank.get_fragment() + Fragment(comb)