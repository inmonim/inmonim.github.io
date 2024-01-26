arr = [[2] for i in range(3)]

new_arr = arr.copy()

# new_arr[0][1]= 5

new_arr[0] = 5

print(arr)
print(new_arr)

print(arr[0] is new_arr[0])