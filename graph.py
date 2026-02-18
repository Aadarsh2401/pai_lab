def input_graph():
    graph={}
    
    n=int(input("Enter number of nodes"))
    for i in range(n):
        node=input("Enter node name")
        graph[node]=[]
        
    e=int(input("Enter number of edges"))
    for j in range(e):
        u=input("From: ")
        v=input("To: ")
        graph[u].append(v)
        graph[v].append(u)
        
        
    return graph



graph = input_graph()
print("Graph:",graph)
