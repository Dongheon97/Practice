import heapq
import sys
input = sys.stdin.readline

INF = int(1e9)

n, m = map(int, input().split())
start = int(input)

graph = [[] for i in range(n+1)]
# visited = [False]*(n+1)
distance = [INF] *(n+1)

# 간선 정보 입력 받기
for _ in range(m):
    a, b, c = map(int, input().split())
    graph[a].append((b, c)) # cost c of a -> b

# def get_smallest_node():
#     min_value = INF
#     index = 0 # shortest node(index)
#     for i in range(1, n+1):
#         if (distance[i] < min_value) and (not visited[i]):
#             min_value = distance[i]
#             index = i
#     return index

# def dijkstra(start):                                                              # O(V**2)
#     distance[start] = 0 # init start node
#     visited[start] = True
#     for j in graph[start]: 
#         distance[j[0]] = j[1]
#     for i in range(n-1):        # 시작 노드를 제외한 전체 n-1 개 노드에 대해 반복
#         now = get_smallest_node()   # 최단 거리가 가장 짧은 노드를 꺼내 방문처리
#         visited[now] = True
#         for j in graph[now]:
#             cost = distance[now] + j[1] # 현재 노드와 연결된 다른 노드를 확인
#             if cost<distance[j[0]]:
#                 distance[j[0]] = cost

def dijkstra_heap(start):           # O(ElogV)
    q = []
    # 시작 노드로의 최단 경로 0으로 설정, 큐에 삽입
    heapq.heappush(q, (0, start))
    distance[start] = 0
    while q:                            # 큐가 비어있지 않다면
        # 최단거리 짧은 노드 정보 꺼내기
        dist, now = heapq.heappop(q)
        if distance[now] < dist:        # 현재 노드가 이미 처리된 적이 있으면 무시
            continue
        for i in graph[now]:
            cost = dist + i[1]
            # 현재 노드를 거쳐서, 다른 노드로 이동하는 거리가 더 짧은 경우
            if cost<distance[i[0]]:
                distance[i[0]] = cost
                heapq.heappush(q, (cost, i[0]))


dijkstra_heap(start)

for i in range(1, n+1):
    if distance[i] == INF:
        print("INFINITY")
    else:
        print(distance[i])


