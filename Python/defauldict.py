a_size, b_size = input().split()
a_size = int(a_size)
b_size = int(b_size)

a = []
b = []

for i in range(a_size):
    a.append(input())
for i in range(b_size):
    b.append(input())
for i in b:
    for j in range(len(a)):
        if i == a[j]:
            print(j+1, end=" ")
    print()