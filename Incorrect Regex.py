import re

n = int(input())

for _ in range(0, n, 1):
    i = input()
    an = re.search('^(?![A-Z]+$)(?![a-z]+$)(?!\d+$)(?![\W_]+$)\S{8,}$', i)
    if an:
        print('True')
    else:
        print('False')