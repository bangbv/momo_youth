#!/bin/python3

import math
import os
import random
import re
import sys

from pandas import pivot

#
# Complete the 'quickSort' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY arr as parameter.
#
    
def quickSort(arr):
    # Write your code here
    pivot = arr[0]
    left, right, equal = [], [], []
    for i in arr:
        if i > pivot:
            right.append(i)
        elif i < pivot:
            left.append(i)
        elif i == pivot:
            equal.append(i)
    res = left + equal + right
    return res, pivot

if __name__ == '__main__':


    n = int(input().strip())

    arr = list([6, 5, 2, 8, 3, 7, 3, 8,3, 7, 2, 7, 2, 7, 3, 7 ,4 ,655,4 ,7 ,4 ,74])

    result, pivot = quickSort(arr)

    print(result, pivot)
