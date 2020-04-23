# 8. 
# Вводятся три разных числа. 
# Найти, какое из них является средним (больше одного, но меньше другого).

a = int(input('Первое число: '))
b = int(input('Второе число: '))
c = int(input('Третье число: '))

if ((a < b) and (a > c)) or ((a < c) and (a > b)):
    print(a)

if ((b < c) and (b > a)) or ((b < a) and (b > c)):
    print(b)

if ((c < a) and (c > b)) or ((c < b) and (c > a)):
    print(c)
