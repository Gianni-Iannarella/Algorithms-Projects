def mystery(arr):
    k = 0
    res = 0
    while k < len(arr):
        res += (arr[k])
        
        k += 2
    return res

def mystery2(arr):
    res = 0
    for i in range(0, len(arr), 2):
        res += arr[i]
    return res



array = [1,2,3,4,5,6,7,8] 
print(mystery(array))
print(mystery2(array))

