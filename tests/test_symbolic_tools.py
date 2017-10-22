import unittest
from symengine import Function, Symbol, sin, Integer
from jitcxde_common.symbolic_tools import collect_arguments, count_calls, has_function

f = Function("f")
g = Function("g")
a = Symbol("a")

class TestCollectArguments(unittest.TestCase):
	def test_complex_expression(self):
		expression = 3**f(42) + 23 - f(43,44) + f(45+a)*sin( g(f(46,47,48)+17) - g(4) )
		
		self.assertEqual(
				collect_arguments(expression,f),
				{
					(Integer(42),),
					(Integer(43), Integer(44)),
					(45+a,),
					(Integer(46), Integer(47), Integer(48))
				}
			)
		
		self.assertEqual(count_calls(expression,f),4)
		self.assertTrue(has_function(expression,f))
	
	def test_function_within_function(self):
		expression = f(f(42))
		
		self.assertEqual(
				collect_arguments(expression, f),
				{ (Integer(42),) , (f(Integer(42)),) }
			)
		
		self.assertEqual(count_calls(expression,f),2)
		self.assertTrue(has_function(expression,f))
	
	def test_no_function(self):
		expression = g(a)+42
		
		self.assertEqual( collect_arguments(expression,f), set() )
		self.assertEqual(count_calls(expression,f),0)
		self.assertFalse(has_function(expression,f))


if __name__ == "__main__":
	unittest.main(buffer=True)