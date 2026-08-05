import ctypes
import Metal
import objc
import struct

add_kernel = '''
#include <metal_stdlib>

using namespace metal;

kernel 
void add (
  device const float* input1,
  device const float* input2,
  device float* result,
  uint thread_id [[thread_position_in_grid]])
{
  result[thread_id] = input1[thread_id] + input2[thread_id];
}
'''

arr_sz = 8
inp1 = [float(1.0) for i in range(arr_sz)]
inp2 = [float(4.0) for i in range(arr_sz)]

if __name__ == "__main__":
  c_arr_type = ctypes.c_float * arr_sz

  res_arr  = c_arr_type()
  inp1_arr = c_arr_type(*inp1)
  inp2_arr = c_arr_type(*inp2)

  device   = Metal.MTLCreateSystemDefaultDevice()

  in1_buf  = device.newBufferWithBytes_length_options_(inp1_arr, ctypes.sizeof(inp1_arr), Metal.MTLResourceStorageModeShared)
  in2_buf  = device.newBufferWithBytes_length_options_(inp2_arr, ctypes.sizeof(inp2_arr), Metal.MTLResourceStorageModeShared)
  res_buf  = device.newBufferWithBytes_length_options_(res_arr, ctypes.sizeof(res_arr), Metal.MTLResourceStorageModeShared)

  lib, err = device.newLibraryWithSource_options_error_(add_kernel, None, None)
  func = lib.newFunctionWithName_("add")
  pipeline, err = device.newComputePipelineStateWithFunction_error_(func, None)

  cmd_que  = device.newCommandQueue()
  cmd_buff = cmd_que.commandBuffer()
  cmd_enc  = cmd_buff.computeCommandEncoder()

  cmd_enc.setBuffer_offset_atIndex_(in1_buf, 0, 0)
  cmd_enc.setBuffer_offset_atIndex_(in2_buf, 0, 1)
  cmd_enc.setBuffer_offset_atIndex_(res_buf, 0, 2)

  cmd_enc.setComputePipelineState_(pipeline)

  cmd_enc.dispatchThreads_threadsPerThreadgroup_(
    Metal.MTLSizeMake(arr_sz, 1, 1),
    Metal.MTLSizeMake(1, 1, 1)
  )

  cmd_enc.endEncoding()
  cmd_buff.commit()
  cmd_buff.waitUntilCompleted()

  raw_tupl  = res_buf.contents().as_tuple(ctypes.sizeof(res_arr))
  raw_bytes = b''.join(raw_tupl)
  result    = list(struct.unpack(f'<{arr_sz}f', raw_bytes))