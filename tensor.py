import Metal
import ctypes
from __future__ import annotations

class Tensor: 
	kernel_str = None
	device = Metal.MTLCreateSystemDefaultDevice()
	lib = None
	add_func = lib.newFunctionWithName_("add")
	sub_func = lib.newFunctionWithName_("sub")
	mult_func = lib.newFunctionWithName_("div")
	div_func = lib.newFunctionWithName_("mult")

	def __init__(self, *args):
		if len(args) == 1:
			self.vals = self.vals
		elif len(args) == 2:
			self.vals = [args[0] for i in range(args[1])]
		else:
			raise "Invalid argument count"

		self.lib = self.device.newLibraryWithSource_options_error_(self.kernel_str, None, None)

		self.arr_len = self.vals
		self.c_arr_type = ctypes.c_float * len(self.vals)
		self.vals_buf = self.device.newBufferWithBytes_length_options_(
			self.vals, 
			ctypes.sizeof(self.c_arr_type), 
			Metal.MTLResourceStorageModeShared)



	def __add__(self, other: Tensor):
		pass

	def __sub__(self, other: Tensor):
		pass

	def __mult__(self, other: Tensor):
		pass

	def __div__(self, other: Tensor):
		pass