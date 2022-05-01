from collections import deque
from turtle import Turtle

def dfs(graph, v, visited):
    # 현재 노드 방문처리
    visited[v] = True
    print(v, end=" ")
    # 연결된 노드 재귀 방문
    for i in graph[v]:
        if not visited[i]:
            dfs(graph, i, visited)

def dfs(graph, v, visited):
    visited[v] = True
    print(v, end=" ")
    for i in graph[v]:
        if not visited[i]:
            dfs(graph, i, visited)

def bfs(graph, start, visited):
    queue = deque([start])
    visited[start] = True
    while queue:
        v = queue.popleft()
        print(v, end=" ")
        for i in graph[v]:
            if not visited[i]:
                visited[v] = True
                queue.append(i)
    
def ddfs(x, y):
    if x<=-1 or x>=n or y<=-1 or y>=m:
        return False
    if graph[x][y]==0:
        graph[x][y]=1
        ddfs(x-1, y)
        ddfs(x+1, y)
        ddfs(x, y-1)
        ddfs(x, y+1)
        return True
    return False

def bbfs(sx, sy):
    queue = deque()
    queue.append((sx, sy))
    while queue:
        ix, iy = queue.popleft()
        
        for i in range(4):
            nx = ix + dx[i]
            ny = iy + dy[i]
            if nx<0 or nx>=n or ny<0 or ny>=m:
                continue
            if graph[nx][ny] == 0:
                continue
            if graph[nx][ny] == 1:
                graph[nx][ny] = graph[ix][iy] + 1
                queue.append((nx, ny))
    return graph[n-1][m-1]

def bfs(graph, start, visited):
    # queue
    queue = deque([start])
    # 방문처리
    visited[start] = True
    # until queue empty
    while queue:
        # extract queue
        v = queue.popleft()
        print(v, end=" ")
        # insert queue
        for i in graph[v]:
            if not visited[i]:
                queue.append(i)
                visited[i] = True

if __name__=="__main__":
    d_graph = [
        [],
        [2, 3, 8],
        [1, 7],
        [1, 4, 5],
        [3, 5],
        [3, 4],
        [7],
        [2, 6, 8],
        [1, 7]
    ]
    b_graph = [
        [],
        [2, 3, 8],
        [1, 7],
        [1, 4, 5],
        [3, 5],
        [3, 4],
        [7],
        [2, 6, 8],
        [1, 7]
    ]
    d_visited = [False]*9
    b_visited = [False]*9
    dfs(d_graph, 1, d_visited)
    print()
    bfs(b_graph, 1, b_visited)

    n, m = map(int, input().split())

    graph = []
    for i in range(n):
        graph.append(list(map(int, input().split())))

        result = 0
        for i in range(n):
            for j in range(m):
                if ddfs(i, j)==True:
                    result+=1
    print(result)

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    print(bfs(0,0))

