total = 0
n = int(input())
m = input().strip().split()
for i in range(n):
    inp = input().strip().split()
    for a in range(len(inp)):
        if m[a] == "MARKS":
            total += int(inp[a])
print(total/n)