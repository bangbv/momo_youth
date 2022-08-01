if __name__ == '__main__':
    scores = []
    names = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        scores.append(score)
        names.append(name)
    max_score = max(scores)
    min_score = min(scores)
    for i in scores:
        if max_score > i > min_score:
            max_score = i
    name = []
    for i in range(len(scores)):
        if scores[i] == max_score:
            name.append(names[i])
    name.sort()
    for i in name:
        print(i)