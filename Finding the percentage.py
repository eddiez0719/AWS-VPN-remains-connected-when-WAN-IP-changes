n = int(input())
l = []
total = 0
for _ in range(0, n, 1):
    m = input().split()
    l.append(m)
#[['edd', '25', '26.5', '22'], ['dan', '11', '88', '19']]
#print(l)
v = input()
for item in l:
    if v == item[0]:
        for i in range(1, len(item)):
            total +=float(item[i])
        print('%.2f '% float((total)/(len(item)-1)))
    #if v in l:
        #print(v)
    # for i in range(1, len(m)):
    #     total +=float(m[i])
    #     #print(m[i], end='')
    # print(float(total / 3))
    # print('%.2f '% float(total/3))
