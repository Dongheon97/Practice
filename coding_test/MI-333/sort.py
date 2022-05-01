import heapq

def insertion(arr):                                         # O(N**2)
    iarr = arr.copy()
    for i in range(1, len(iarr)):
        for j in range(i, 0, -1):
            if(iarr[j]<iarr[j-1]):
                iarr[j], iarr[j-1] = iarr[j-1], iarr[j]
            else:
                break
    print(iarr)


def quick(qarr, start, end):                                    # O(NlogN)
    if (start>=end):
        return
    pivot = start
    left = start+1
    right = end
    while(left <= right):
        while(left <= end and qarr[left] <= qarr[pivot]):
            left+=1
        while(right>start and qarr[right] >= qarr[pivot]):
            right-=1
        if(left>right):
            qarr[right], qarr[pivot] = qarr[pivot], qarr[right]
        else:
            qarr[left], qarr[right] = qarr[right], qarr[left]
    quick(qarr, start, right-1)
    quick(qarr, right+1, end)
    
def select(arr):                                               # O(v**2)
    sarr = arr.copy()
    for i in range(len(sarr)):
        index = i
        for j in range(i+1, len(sarr)):
            if(sarr[j]<sarr[index]):
                index = j
        sarr[index], sarr[i] = sarr[i], sarr[index]
    print(sarr)

def insert(array):
    iarr = array.copy()
    for i in range(1, len(iarr)):
        for j in range(i, 0, -1):
            if (iarr[j] < iarr[j-1]):
                iarr[j-1], iarr[j] = iarr[j], iarr[j-1]

    print(iarr)

def quicksort(arr, start, end):
    if(start>=end):
        return
    pivot = start
    left = start+1
    right = end
    while(left<=right):
        while(left<=end and arr[pivot]>arr[left]):
            left+=1
        while(right>start and arr[pivot]<arr[right]):
            right-=1
        if(left>right):
            arr[right], arr[pivot] = arr[pivot], arr[right]
        else:
            arr[left], arr[right] = arr[right], arr[left]
    quicksort(arr, start, right-1)
    quicksort(arr, right+1, end)

import heapq

# 최소 힙
def minheap(iterable):
    h = []
    result = []
    # 모든 원소를 차례대로 힙에 삽입
    for value in iterable:
        heapq.heappush(h, value)
    # 힙에 삽입된 모든 원소를 차례대로 꺼내어 담기
    for i in range(len(h)):
        result.append(heapq.heappop(h))
    print(result)
    return result

# 최대 힙
def maxheap(iterable):
    h = []
    result = []
    # 모든 원소를 차례대로 힙에 삽입
    for value in iterable:
        heapq.heappush(h, -value)
    # 힙에 삽입된 모든 원소를 차례대로 꺼내어 담기
    for i in range(len(h)):
        result.append(-heapq.heappop(h))
    print(result)
    return result


if __name__=="__main__":
    arr = [7, 5, 9, 0, 3, 1, 6, 2, 4, 8]
    select(arr)
    insert(arr)
    print()
    minheap(arr)
    maxheap(arr)
    print()
    quicksort(arr, 0, 9)
    # quick(arr, 0, 9)
    print(arr)