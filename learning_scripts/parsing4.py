a = int(input())
b = int(input())
c = (a + b)/10

if c < 1:
    print(f'Полученное число меньше 1 и равно {c}')
elif c > 1:
    print(f'Полученное число больше 1 и равно {c}')
else:
    print(f'Полученное число равно 1')