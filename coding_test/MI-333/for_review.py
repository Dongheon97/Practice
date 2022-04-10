# Permutation
from itertools import permutations
data = ['A ', 'B', 'C', 'D']
p_result = list(permutations(data, 3))
print(p_result)
print(len(p_result))

# Combination 
from itertools import combinations
data = ['A', 'B', 'C', 'D']
c_result = list(combinations(data, 2))
print(c_result)
print(len(c_result))

n = int(input())
data = list(map(int, input().split())) # 공백 기준으로 문자열 받아 정수로 바꾼다.

data.sort(reverse=True)
print(data)

# 많은 양의 데이터를 입력 받을 때
import sys
data = sys.stdin.readline().rstrip() # 줄 단위로 입력 받고 줄바꿈 기호 삭제
print(data)

