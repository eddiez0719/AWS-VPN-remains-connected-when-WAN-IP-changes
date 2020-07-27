n = int(input())
for _ in range (0,n,1):
    try:
        a1, b1 = input().split()
        print(int(int(a1)/int(b1)))
    except ZeroDivisionError as e:
        print('Error Code:' + str(e))
    except ValueError as v:
        print('Error Code:' + str(v))
