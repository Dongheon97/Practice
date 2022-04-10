#data = list(map(int, input().split()))
givenNum = input()
data = []
for i in range(len(givenNum)):
    #print(givenNum[i:i+1])
    data.append(int(givenNum[i:i+1]))
print(data)
sum = 0
for i in range(len(data)): 
    if(data[i]==0 or data[i]==1):
        sum += data[i]
    else:
        if(sum == 0):
            sum += data[i]
        else:
            sum *= data[i]

print(sum)

from curses.ascii import isalpha
isalpha()
# data = list(map(int, input().split()))

# n = data[0]
# k = data[1]

# count = 0
# while n!=1:
#     if (n % k) != 0:
#         n -= 1
#         count += 1
#     else:
#         n = n//k
#         count += 1
# print(count)

