#!/usr/bin/env python
# nine.py - a postfix calculator for python 3 (python 2 support incoming)
# version 9-dev    2019-04-06

from __future__ import print_function, division

import readline, inspect, cmath, math, re

import sys
sys.setrecursionlimit(100)

def is_number(s):
	try:
		complex(s)
		return True
	except ValueError:
		return False

def countFunctionArguments(func):
	try:
		return len(inspect.signature(func).parameters)
	except:
		return len(inspect.getargspec(func).args)


class Calculator:
	def __init__(self):
		self.operations = {
			'+' : lambda a,b:a+b,
			'-' : lambda a,b:b-a,
			'/' : lambda a,b:b / a,
			'*' : lambda a,b:a*b,
			'**' : lambda a,b:a ** b,
		
			'sin' : lambda a:a.trigfunc(cmath.sin),
			'cosec' : lambda a:a.trigfunc(cmath.sin).inverse(),
			'cos' : lambda a:a.trigfunc(cmath.cos),
			'sec' : lambda a:a.trigfunc(cmath.cos).inverse(),
			'tan' : lambda a:a.trigfunc(cmath.tan),
			'cot' : lambda a:a.trigfunc(cmath.tan).inverse(),
		
			'atan' : lambda a:a.trigfunc(cmath.atan),
			'asin' : lambda a:a.trigfunc(cmath.asin),
			'acos' : lambda a:a.trigfunc(cmath.acos),
		
			'sqrt' : lambda a:a.pow(Symbol(1/2.0)),
			'cbrt' : lambda a:a.pow(Symbol(1/3.0)),
			'isqrt' : lambda a:a.pow(Symbol(1/2.0)).inverse(),
			'icbrt' : lambda a:a.pow(Symbol(1/3.0)).inverse(),
		
			'%' : lambda a,b:b.modulo(a),
			'ln' : lambda a:a.log(),
			'log' : lambda a,b:a.log(b),
			'rad' : lambda a:a.trigfunc(lambda z: math.radians(z.real)),
			'deg' : lambda a:a.trigfunc(lambda z: math.degrees(z.real)),
	
			'arg' : lambda a:a.trigfunc(cmath.phase),
			'abs' : lambda a:a.trigfunc( lambda z:math.hypot(z.real, z.imag) ),
			'Re' : lambda a:a.real,
			'Im' : lambda a:a.imag,
	
			'=': lambda a,b:self.variableAssign(a,b)
		}
		
		self.stack = []
		self.variables = {}
		self.variables = {
			Symbol(self, 'pi'): Symbol(self, math.pi),
			Symbol(self, 'e'): Symbol(self, math.e),
			Symbol(self, '\\'): Symbol(self, 0)
		}
	
	def execute(self, string):
		'''
			Execute a postfix string until no operations remain.
			Assumes that operation arity conditions are already met,
			and will raise errors if not.
			
			The stack is cleared before execution begins.
			After execution, the stack is assigned to the \ (backslash)
			variable.
		'''
		# self.stack.clear()
		del self.stack[:]
		symbols = [Symbol(self, s) for s in string.split()]
		
		search = next(
			((index, sym) for index, sym in enumerate(symbols) \
			if sym.type == Symbol.Operation), None)
		
		while search:
			index, oper = search
			func = self.operations[oper.value]
			args = countFunctionArguments(func)
			
			popped = symbols[index-args:index][::-1]
			result = func(*popped)
			if result: symbols.insert(index+1, result)
			del symbols[index-args:index+1]
			
			search = next(
				((index, sym) for index, sym in enumerate(symbols) \
				if sym.type == Symbol.Operation), None)
		
		self.stack += [sym if sym not in self.variables else self.variables[sym] for sym in symbols]
		self.variableAssign(Symbol(self, '\\'), self.stack[-1])
	
	def variableAssign(self, variableSymbol, value):
		self.variables[variableSymbol] = value
	
	def __str__(self):
		return str([i.value for i in self.stack])

class Symbol:

	Types = ['number', 'dimension', 'variable', 'operation']
	Number = Types[0]
	Dimension = Types[1]
	Variable = Types[2]
	Operation = Types[3]
	
	@property
	def type(self):
		return self._type
	
	@type.setter
	def type(self, newval):
		if newval not in Symbol.Types:
			raise ValueError('Invalid type: {}'.format(newval))
		self._type = newval
		
	@property
	def value(self):
		if self.type == Symbol.Variable:
			# print(self)
			# return self.calc.variables.get(self, Symbol(self.calc, 0))._value
			if self in self.calc.variables:
				return self.calc.variables[self].value
			else:
				return self._value
		
		return self._value
	
	def __init__(self, calc, value):
		self.calc = calc
		self._type = None
		
		if is_number(value):
			self._type = Symbol.Number
			self._value = complex(value)
			
		elif value in self.calc.operations:
			self._type = Symbol.Operation
			self._value = value
			
		elif value.isalpha() or value == '\\':
			self._type = Symbol.Variable
			self._value = value
		
		else:
			raise ValueError('Failed to resolve Symbol type: {}'.format(value))
	
	def __add__(self, other): return Symbol(self.calc, self.value + other.value)
	def __sub__(self, other): return Symbol(self.calc, self.value - other.value)
	def __mul__(self, other): return Symbol(self.calc, self.value * other.value)
	def __truediv__(self, other): return Symbol(self.calc, self.value / other.value)
	def __pow__(self, other): return Symbol(self.calc, self.value**other.value)
	
	def inverse(self):
		return Symbol(self.calc, 1.0 / self.value)
	
	def trigfunc(self, func):
		pass
	
	def __str__(self):
		return 'Symbol({})'.format(self._value)
	
	def __repr__(self):
		return 'Symbol({}, {})'.format(self._value, self.type)
	
	def __eq__(self, other):
		# print('eq', self, other)
		return other._value == self._value and other.type == self.type
	
	def __hash__(self):
		return hash(self._value)

if __name__ == '__main__':
	c = Calculator()
	
	try:
		raw_input
	except:
		raw_input = input
	
	while 1:
		i = raw_input('> ')
		c.execute(i)
		print(c)
	
	c.execute('4 6 + 2 / a = a a +')
	# c.execute('4 6 +')
	print(c.stack)
	print(c.variables)
	
	if 0:
		x = Symbol(c, 10)
		y = Symbol(c, 7)
		result = x + y
		print(result)
		result = x - y
		print(result)
		result = x * y
		print(result)
		result = (x / y).inverse()
		print(result)
	
		x = Symbol(c, 2-2j)
		y = Symbol(c, 5+1j)
		print(y ** x)
