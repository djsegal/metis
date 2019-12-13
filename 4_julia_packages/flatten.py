import functools
import operator

def flatten(cur_input):

  is_container = hasattr(cur_input, '__len__')
  is_container &= not isinstance(cur_input, str)

  if not is_container : return [ cur_input ]

  return functools.reduce(
    operator.concat, map(flatten, cur_input)
  )
