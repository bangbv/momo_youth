if __name__ == '__main__':
    records = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        records.append([name, score])
    
    lowest_score = 100
    sec_lowest_score = 100
    for record in records:
        if record[1] < lowest_score:
            lowest_score = record[1]
    student = []    
    for record in records:
        if record[1] < sec_lowest_score and record[1] > lowest_score:
            sec_lowest_score = record[1]
            
    for record in records:
        if record[1] == sec_lowest_score:
            student.append(record[0])
    
    
    student.sort()
    for i in student:
        print(i)    
