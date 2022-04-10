# Ant soldier
n = int(input)
array = list(map(int, input().split()))
d = [0]*100
d[0] = array[0]
d[1] = max(array[0], array[1])
for i in range(2, n):
    d[i] = max(d[i-1], d[i-2]+array[i])
print(d[n-1]) # Answer

# -1, /5, /3, /2
x = int(input())
d = [0]*30001
for i in range(2, x+1):
    d[i] = d[i-1] + 1 # -1
    if(d[i]%5 == 0):
        d[i] = min(d[i], d[i//5]+1) # 5의 배수
    if(d[i]%3 == 0):
        d[i] = min(d[i], d[i//3]+1) # 3의 배수
    if(d[i]%2 == 0):
        d[i] = min(d[i], d[i//2]+1) # 2의 배수
print(d[x])

# make least of coin
n, m = map(int, input().split())
coin = []
for i in range[n]:
    coin.append(int(input()))
d=[10001]*(m+1)

d[0] = 0
for i in range(n):
    for j in range(coin[i], m+1):
        if(d[j-coin[i]] != 10001):
            d[j] = min(d[j], d[j-array[i]]+1)
if d[m] == 10001:
    print(-1)
else:
    print(d[m])


# L
n = int(input())
array = list(map(int, input().split()))
array.reverse()

dp = [1]*n
for i in range(1, n):
    for j in range(0, i):
        if(array[j]<array[i]):
            dp[i] = max(d[i], d[j]+1)
print(n-max(dp))