if __name__ == '__main__':
    n = int(input())
    arr = input().split()
    for i in range(len(arr)):
        arr[i] = int(arr[i])
    max_score = max(arr)
    min_score = min(arr)
    for i in arr:
        if i > min_score and i < max_score:
            min_score = i
    print(min_score)
