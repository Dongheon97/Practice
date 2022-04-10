import time

from pyparsing import java_style_comment

# def fibo(givenNum):
#     if givenNum == 0:
#         return 0
#     elif givenNum == 1:
#         return 1
#     elif givenNum == 2:
#         return 1
#     else:
#        return fibo(givenNum-1) + fibo(givenNum-2)

# def fibo(givenNum):
#     if givenNum<=2:
#         return 1
    
#     a = 0
#     b = 1
#     for _ in range(givenNum-1):
#         a, b = b, a+b
#     return b

# def fibo(givenNum):
#     fibo_cache = []
#     for i in range(givenNum):
#         if (i<2):
#             fibo_cache.append(1)
#         else:
#             fibo_value = fibo_cache[i-2] + fibo_cache[i-1]
#             fibo_cache.append(fibo_value)
#     return fibo_cache[givenNum-1]

def fibo(x):
    ret = []
    for i in range(x):
        if(i<2):
            ret.append(1)
        else:
            ret.append(ret[i-1]+ret[i-2])
    return ret[x-1]


if __name__ =="__main__":
    # givenNum = int(input())
    start = time.time()
    result_fibo = fibo(30)
    end = time.time()
    print(result_fibo)
    print(round((end-start)*1000, 4))
