import ctypes
import os
#import numpy
#import pywasm
from Set_Up import *

path = os.getcwd()
library = ctypes.CDLL(os.path.join(path, 'Pathfind.so'))


def c_path_finder(flags, start_coordinates, target_coordinates):
    for I, flag_list in enumerate(flags):
         flags[I] = tuple(flag_list)
    array_flags = (ctypes.c_bool * len(flags[0]) * len(flags))(*tuple(flags))
    array_start_coordinates = (ctypes.c_int * len(start_coordinates))(*start_coordinates)
    array_target_coordinates = (ctypes.c_int * len(target_coordinates[0]) * len(target_coordinates))(*target_coordinates)
    library.path_finder(len(flags),len(flags[0]), len(target_coordinates), array_flags, array_start_coordinates, array_target_coordinates)

def c_maze_visualizer(flags):
     for I, flag_list in enumerate(flags):
         flags[I] = tuple(flag_list)
     test_flags = (ctypes.c_bool * len(flags[0]) * len(flags))(*tuple(flags))
     library.maze_visualizer(len(flags), len(flags[0]), test_flags)

def c_debug(flags, start_coordinates, target_coordinates):
    print(start_coordinates)
    for I, flag_list in enumerate(flags):
         flags[I] = tuple(flag_list)
    array_flags = (ctypes.c_bool * len(flags[0]) * len(flags))(*tuple(flags))
    array_start_coordinates = (ctypes.c_int * len(start_coordinates))(*start_coordinates)
    array_target_coordinates = (ctypes.c_int * len(target_coordinates[0]) * len(target_coordinates))(*target_coordinates)
    library.debug(len(flags[0]), len(flags), len(target_coordinates), array_flags, array_start_coordinates, array_target_coordinates)

if __name__ == '__main__':
  sample = [[True, False, False],[True, False, True]]
  c_debug(sample, (0, 0), [(1, 2),(0, 2)])
