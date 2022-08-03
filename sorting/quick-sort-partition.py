#!/bin/python3

import math
import os
import random
import re
import sys

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
    return res

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    arr = list(map(int, input().rstrip().split()))

    result = quickSort(arr)

    fptr.write(' '.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
