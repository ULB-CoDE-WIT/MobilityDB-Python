from MobilityDB.TemporalTypes import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS


class TBool(Temporal):
	"""
	Temporal booleans of any duration (abstract class)
	"""

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		if value[0] != '{' and value[0] != '[' and value[0] != '(':
			return TBoolInst(value)
		elif value[0] == '[' or value[0] == '(':
			return TBoolSeq(value)
		elif (value[0] == '{'):
			if value[1] == '[' or value[1] == '(':
				return TBoolS(value)
			else:
				return TBoolI(value)
		raise Exception("ERROR: Could not parse temporal float value")

	@staticmethod
	def write(value):
		if not isinstance(value, TBool):
			raise ValueError('TBool value must subclass TBool class')
		return value.__str__().strip("'")


class TBoolInst(TemporalInst, TBool):
	"""
	Temporal booleans of instant duration
	"""

	def __init__(self, value, time=None):
		TemporalInst.BaseClass = bool
		super().__init__(value, time)


class TBoolI(TemporalI, TBool):
	"""
	Temporal booleans of instant set duration
	"""

	def __init__(self,  *argv):
		TemporalI.BaseClass = bool
		TemporalI.ComponentClass = TBoolInst
		super().__init__(*argv)


class TBoolSeq(TemporalSeq, TBool):
	"""
	Temporal booleans of sequence duration
	"""

	def __init__(self, instantList, lower_inc=None, upper_inc=None, interp='Stepwise'):
		TemporalSeq.BaseClass = bool
		TemporalSeq.BaseClassDiscrete = True
		TemporalSeq.ComponentClass = TBoolInst
		self._interp = 'Stepwise'
		super().__init__(instantList, lower_inc, upper_inc)

	@classmethod
	def interpolation(self):
		return 'Stepwise'


class TBoolS(TemporalS, TBool):
	"""
	Temporal booleans of sequence set duration
	"""

	def __init__(self, sequenceList, interp='Stepwise'):
		TemporalS.BaseClass = bool
		TemporalS.BaseClassDiscrete = True
		TemporalS.ComponentClass = TBoolSeq
		self._interp = 'Stepwise'
		super().__init__(sequenceList)

	@classmethod
	def interpolation(self):
		return 'Stepwise'

