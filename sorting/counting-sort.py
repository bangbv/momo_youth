#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'countingSort' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY arr as parameter.
#

def countingSort(arr):
    # Write your code here
    arr_len = len(arr)
    output = [0] * arr_len
    count = [0] * (max(arr)+1)
    if arr_len == max(arr)+2:
        count.append(0)
    for i in arr:
        count[int(i)] += 1
    for i in range(len(count)):
        if i+1 < len(count):
            count[i+1] = count[i] + count[i+1]
    for i in arr:
        if output[count[i]-1] == 0:
            output[count[i]-1] = i
        else:
            for a in range(2, len(output)):
                if output[count[i]-a] == 0:
                    output[count[i]-a] = i
                    break
    return output

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    arr = list(map(int, input().rstrip().split()))

    result = countingSort(arr)

    fptr.write(' '.join(map(str, result)))
    fptr.write('\n')

    fptr.close()