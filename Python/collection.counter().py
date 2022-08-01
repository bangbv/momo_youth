num_of_shoes = int(input())
shoe_list = input().split()
num_of_customer = int(input())
total = 0
for i in range(num_of_customer):
    customer = input().split()
    if customer[0] in shoe_list:
        total += int(customer[1])
        shoe_list.remove(customer[0])
print(total)