from numpy import Inf


graph_size = 9
graph = []
for i in range(graph_size):
    graph.append([])
    for j in range(graph_size):
        graph[i].append(0)


start = 0

graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
        [4, 0, 8, 0, 0, 0, 0, 11, 0],
        [0, 8, 0, 7, 0, 4, 0, 0, 2],
        [0, 0, 7, 0, 9, 14, 0, 0, 0],
        [0, 0, 0, 9, 0, 10, 0, 0, 0],
        [0, 0, 4, 14, 10, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 1, 6],
        [8, 11, 0, 0, 0, 0, 1, 0, 7],
        [0, 0, 2, 0, 0, 0, 6, 7, 0]
        ]

def dijkstra():
    global start, graph_size
    completed = []
    value = []
    for i in range(graph_size):
        value.append(Inf)
    value[start] = 0 
    
    while len(completed) < graph_size:
        value_not_completed = []
        for i in range(len(value)):
            if i not in completed:
                value_not_completed.append(value[i])
        min_value_index = value.index(min(value_not_completed))

        completed.append(min_value_index)

        for i in range(graph_size):
            if i not in completed and graph[min_value_index][i] != 0:
                if value[i] > value[min_value_index]+graph[min_value_index][i]:
                    value[i] = value[min_value_index]+graph[min_value_index][i]
                        



    for i in range(graph_size):
        print(i, value[i])




    pass
dijkstra()