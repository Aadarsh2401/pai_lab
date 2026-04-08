#input
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


#bfs search

from collections import deque

def bfs(graph, start, goal):
    queue = deque()
    queue.append([start])  # store path, not just node

    visited = set()
    nodes_expanded = 0

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == goal:
            return path, nodes_expanded

        if current not in visited:
            visited.add(current)
            nodes_expanded += 1

            for neighbor in graph[current]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None, nodes_expanded


#dfs search 


def dfs(graph, current, goal, visited=None, nodes_expanded=0):
    if visited is None:
        visited = set()

    visited.add(current)
    nodes_expanded += 1

    if current == goal:
        return [current], nodes_expanded

    for neighbor in graph[current]:
        if neighbor not in visited:
            path, nodes_expanded = dfs(graph, neighbor, goal, visited, nodes_expanded)
            if path:
                return [current] + path, nodes_expanded

    return None, nodes_expanded


path, expanded = dfs(maze, start, goal)

print("Path found:", path)
print("Nodes expanded:", expanded)

import heapq

# Manhattan Distance Heuristic
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Get valid neighbors (Up, Down, Left, Right)
def get_neighbors(node, maze):
    rows = len(maze)
    cols = len(maze[0])
    x, y = node
    
    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if maze[nx][ny] == 0:  # not a wall
                neighbors.append((nx, ny))
    
    return neighbors

#Greeddy best first 
    def greedy_best_first_search(maze, start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), start))
    
    came_from = {}
    visited = set()
    nodes_expanded = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        if current in visited:
            continue

        visited.add(current)
        nodes_expanded += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                heapq.heappush(open_list, (heuristic(neighbor, goal), neighbor))
                came_from[neighbor] = current

    # Reconstruct Path
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from.get(node)
        if node is None:
            print("No Path Found")
            return
    path.append(start)
    path.reverse()

    print("Greedy Path:", path)
    print("Nodes Expanded:", nodes_expanded)

#a star search
    def a_star_search(maze, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    came_from = {}
    g_cost = {start: 0}
    nodes_expanded = 0

    while open_list:
        _, current = heapq.heappop(open_list)
        nodes_expanded += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current, maze):
            tentative_g = g_cost[current] + 1

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f, neighbor))
                came_from[neighbor] = current

    # Reconstruct Path
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from.get(node)
        if node is None:
            print("No Path Found")
            return
    path.append(start)
    path.reverse()

    print("A* Path:", path)
    print("Nodes Expanded:", nodes_expanded)


#rbfs
def rbfs(maze, current, goal, g, f_limit, path, nodes_expanded):
    nodes_expanded[0] += 1

    if current == goal:
        return path, 0

    successors = []
    for neighbor in get_neighbors(current, maze):
        if neighbor not in path:
            new_g = g + 1
            f = new_g + heuristic(neighbor, goal)
            successors.append((f, neighbor, new_g))

    if not successors:
        return None, math.inf

    while True:
        successors.sort(key=lambda x: x[0])
        best_f, best_node, best_g = successors[0]

        if best_f > f_limit:
            return None, best_f

        alternative = successors[1][0] if len(successors) > 1 else math.inf

        result, best_new_f = rbfs(
            maze,
            best_node,
            goal,
            best_g,
            min(f_limit, alternative),
            path + [best_node],
            nodes_expanded
        )

        successors[0] = (best_new_f, best_node, best_g)

        if result is not None:
            return result, best_new_f


def run_rbfs(maze, start, goal):
    nodes_expanded = [0]
    path, _ = rbfs(maze, start, goal, 0,
                   heuristic(start, goal),
                   [start],
                   nodes_expanded)

    print("RBFS Path:", path)
    print("Nodes Expanded:", nodes_expanded[0])


#ida*

def ida_star_search(maze, start, goal):

    threshold = heuristic(start, goal)
    nodes_expanded = 0

    def dfs(node, g, threshold, path):
        nonlocal nodes_expanded
        nodes_expanded += 1

        f = g + heuristic(node, goal)
        if f > threshold:
            return f

        if node == goal:
            return path

        min_threshold = math.inf

        for neighbor in get_neighbors(node, maze):
            if neighbor not in path:
                result = dfs(neighbor, g+1, threshold, path + [neighbor])

                if isinstance(result, list):
                    return result

                min_threshold = min(min_threshold, result)

        return min_threshold

    while True:
        result = dfs(start, 0, threshold, [start])

        if isinstance(result, list):
            print("IDA* Path:", result)
            print("Nodes Expanded:", nodes_expanded)
            return

        if result == math.inf:
            print("No Path Found")
            return

        threshold = result


#sma*
import heapq

def sma_star(maze, start, goal, memory_limit=10):

    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), 0, start, [start]))

    nodes_expanded = 0

    while open_list:
        f, g, current, path = heapq.heappop(open_list)
        nodes_expanded += 1

        if current == goal:
            print("SMA* Path:", path)
            print("Nodes Expanded:", nodes_expanded)
            return

        for neighbor in get_neighbors(current, maze):
            if neighbor not in path:
                new_g = g + 1
                new_f = new_g + heuristic(neighbor, goal)

                heapq.heappush(open_list, (new_f, new_g, neighbor, path + [neighbor]))

                # Memory control
                if len(open_list) > memory_limit:
                    open_list.sort(reverse=True)  # worst f at front
                    open_list.pop(0)  # remove worst

    print("No Path Found")


def ucs(graph, start, goal):
    priority_queue = [[0, start, [start]]]  # cost, node, path
    visited = set()
    nodes_expanded = 0

    while priority_queue:
        priority_queue.sort(key=lambda x: x[0])
        cost, current, path = priority_queue.pop(0)

        if current == goal:
            return path, cost, nodes_expanded

        if current not in visited:
            visited.add(current)
            nodes_expanded += 1

            for neighbor, weight in graph[current]:
                new_cost = cost + weight
                new_path = path + [neighbor]
                priority_queue.append([new_cost, neighbor, new_path])

    return None, None, nodes_expanded


graph = {
    'A': [('B',10), ('C',25)],
    'B': [('D',40), ('E',5)],
    'C': [('F',15)],
    'D': [('G',30)],
    'E': [('G',60)],
    'F': [('G',5)],
    'G': []
}

path, cost, expanded = ucs(graph, 'A', 'G')

print("Optimal Path:", path)
print("Total Cost:", cost)
print("Nodes Expanded:", expanded)
