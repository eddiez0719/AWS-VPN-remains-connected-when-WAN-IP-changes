from itertools import permutations
n = input().split()
for i in range(1, len(n)):
    data = list(n[0])
    for p in permutations(data, 2):
        print(''.join(p))

#for i in range(0, len(n)):
    # sorted(n[i])
    # print(n[i])
    # data = list(n[0])
    #
    # print(data)
    # for p in permutations(data, 2):
    #     s = sorted(p)
    #     print(''.join(p))
