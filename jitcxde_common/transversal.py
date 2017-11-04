import symengine

class GroupHandler(object):
	"""
	Class to handle groups of synchronised variables for transversal Lyapunov exponents. Main indices are those that represent the normal dynamics, tangent indices are those that belong to tangent vectors.
	"""
	
	def __init__(self,groups):
		self.n = max(max(group) for group in groups)+1
		assert all(all(0<=i<self.n for i in group) for group in groups), "Group elements out of range."
		assert set().union(*groups)==set(range(self.n)), "Groups do not cover all indices."
		assert sum(map(len,groups))==self.n, "Groups overlap."
		
		self.groups = [sorted(group) for group in groups]
	
	@property
	def main_indices(self):
		if not hasattr(self,"_main_indices"):
			self._main_indices = [min(group) for group in self.groups]
		return self._main_indices
	
	@property
	def tangent_indices(self):
		if not hasattr(self,"_tangent_indices"):
			self._tangent_indices = [
					i
					for group in self.groups
					for i in group[1:]
				]
		return self._tangent_indices
	
	def group_from_index(self,index):
		"""returns the number of the group which contains `i`."""
		
		if not hasattr(self,"_group_finder"):
			self._group_finder = {}
			for k,group in enumerate(self.groups):
				for entry in group:
					self._group_finder[entry] = k
		
		return self._group_finder[index]
	
	def iterate(self,iterable):
		"""
		For a main index, return the number of the respective group.
		For a tangent index, returns the respective element and the preceding one in the same group.
		"""
		
		cache = {}
		for k,entry in enumerate(iterable):
			i = self.group_from_index(k)
			try:
				previous_entry = cache[i]
			except KeyError:
				yield i
			else:
				yield previous_entry,entry
			finally:
				cache[i] = entry
	
	def extract_main(self,iterable):
		"""
		Extracts the elements corresponding to the main indices from `iterable`.

		Returns
		-------
		extractor: generator function
			returns an iterator over iterable
		
		extracted_entries : dictionary
			maps an index of a main component to the corresponding element of `iterable`. Note that this only works once `extractor` has been iterated sufficienly far.
		"""
		
		extracted_entries = {}
		def extractor():
			for i,entry in enumerate(iterable):
				if i in self.main_indices:
					extracted_entries[i] = entry
				yield entry
		return extractor,extracted_entries
	
	def back_transform(self,vector):
		if not hasattr(self,"_A_inv"):
			self._A_inv = symengine.zeros(self.n,self.n)
			
			for group in self.groups:
				# Uppercase numbers are indices of the respective submatrix, lowercase numbers are indices of the full matrix
				
				N = symengine.Integer(len(group))
				for I in range(len(group)):
					i = group[I]
					for J in range(1,I+1):
						j = group[J]
						self._A_inv[i,j] = -J/N
					for J in range(I+1,len(group)):
						j = group[J]
						self._A_inv[i,j] = 1-J/N
		
		return self._A_inv*symengine.Matrix(vector)
		
