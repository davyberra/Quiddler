l = [10,8,6,4,2,0]
n = 7
for i, num in enumerate(l):
    if n > num:
        l.insert(i, n)
        break
print(l)