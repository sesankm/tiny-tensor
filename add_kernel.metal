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