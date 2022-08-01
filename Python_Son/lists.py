if __name__ == '__main__':
    N = int(input())
    result = []
    for _ in range(N):
        command = input().split()
        for i in range(1, len(command)):
            command[i] = int(command[i])
        if command[0] == "insert":
            result.insert(command[1], command[2])
        elif command[0] == "print":
            print(result)
        elif command[0] == "remove":
            result.remove(command[1])
        elif command[0] == "append":
            result.append(command[1])
        elif command[0] == "sort":
            result.sort()
        elif command[0] == "pop":
            result.pop()
        elif command[0] == "reverse":
            result.reverse()
        else:
            print("Invalid command!")