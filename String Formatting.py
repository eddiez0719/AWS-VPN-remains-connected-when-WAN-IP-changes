s = 'BANANA'
count = 0
for _ in range(10):
    s1 = input()
    if s1 in s:
        pos = s.find(s1, 0)
        count += 1


