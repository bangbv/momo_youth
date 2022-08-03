#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'bigSorting' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts STRING_ARRAY unsorted as parameter.
#

def merge(arr1, arr2):
     res = arr1 + arr2
     res.sort()
     return res

def bigSorting(unsorted):
     # Write your code here
     arr = []
     for i in range(0, len(unsorted), 2):
          arr.append([unsorted[i], unsorted[i+1]]) if i+1 < len(unsorted) else arr.append([unsorted[i]])
     for i in range(len(arr)):
          arr[i].sort()
     result = []
     while len(arr) != 1:
          if len(arr) == 2:
               result = merge(arr[0], arr[1])
               arr = result
               break
          else:
               for i in range(len(arr)-1, -1, -1):
                    if i-1 > -1 and i % 2 == 0:
                         result.append(merge(arr[i], arr[i-1]))
                    elif i % 2 == 0:
                         result.append(arr[i])
          arr = result
          result = []
     for i in range(len(arr)):
          arr[i] = str(arr[i])
     return arr

if __name__ == '__main__':
     n = int(input().strip())

     unsorted = []

     for _ in range(n):
          unsorted_item = input()
          unsorted.append(int(unsorted_item))

     result = bigSorting(unsorted)

     print(result)