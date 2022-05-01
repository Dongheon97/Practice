from collections import deque

def bfs(ix, iy):
    queue = deque()
    queue.append((ix, iy))
    while queue:
        ix, iy = queue.popleft()

        for i in range(4):
            nx = ix + dx[i]
            ny = iy + dy[i]

            if nx < 0 or nx >= n or ny < 0 or ny >=m:
                continue
            if graph[nx][ny] == 0:
                continue
            
            if graph[nx][ny] == 1:
                graph[nx][ny] = graph[ix][iy] +1
                queue.append((nx, ny))
    return graph[n-1][m-1]




n, m = map(int, input().split())
graph = []
for i in range(n):
    graph.append(list(map(int, input())))

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
print(bfs(0, 0))
