def rec_binary(array, target, start, end):
    if (start > end):
        return None
    mid = (start+end)//2
    if(array[mid] == target):
        return mid
    elif array[mid] > target:
        return rec_binary(array, target, start,  mid-1)
    else:
        return rec_binary(array, target, mid+1, end)
    
def binary(array, target, start, end):                                      # O(logN)
    while(start <= end):
        mid = (start+end) // 2
        if(array[mid] == target):
            return mid
        elif(array[mid] < target):
            start = mid+1
        else:
            end = mid-1
    return None

def rec_binary(array, target, start, end):
    if(start>end):
        return None
    mid = (start+end) // 2
    if(target == array[mid]):
        return mid
    elif(target < array[mid]):
        return rec_binary(array, target, start, mid-1)
    else:
        return rec_binary(array, target, mid+1, end)
    
def binarySearch(array, target, start ,end):
    while(start <= end):
        mid = (start+end)//2
        if(target==array[mid]):
            return mid
        elif(target<array[mid]):
            end = mid-1
        else:
            start = mid+1
    return None
