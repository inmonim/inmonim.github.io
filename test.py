import time

lst = []
start = time.time()

for i in range(100_000_000):
    if i//2 == 0:
        lst.append(i)
    
end = time.time()

print(round(end-start,4))


start2 = time.time()

lst2 = [i for i in range(100_000_000) if i//2 == 0]

end2 = time.time()

print(round(end2-start2, 4))

# start3 = time.time()

# lst3 = [[0 for _ in range(10_000)] for _ in range(10_000)]

# end3 = time.time()

# print(round(end3-start3, 4))


# start4 = time.time()
# lst4 = []

# for _ in range(10_000):
#     tmp_lst = []
#     for _ in range(10_000):
#         tmp_lst.append(0)
#     lst4.append(tmp_lst)

# end4 = time.time()

# print(round(end4-start4, 4))