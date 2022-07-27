if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())
    list = []
    for i in arr:
        if i not in list:
            list.append(i)
    y = 0
    for i in list:
        if i < y:
            y = i
    x = y
    for i in list:
        if i > x:
            x = i      
    for i in list:
        if i > y and i < x:
            y = i       
    print(y)