n = int(input())
total = 0
for _ in range (0, n, 1):
    m = input().split()
v = input()
if v in m:
    for l in m:
        float(l)
        total +=l
    print(total)
    print('%.2f '% (total/3))





