from module import *


front1 = square(int(input('front1= ')))
front2 = circle(int(input('front2 =  ')))

if front1 < front2:
    print(front1, '<', front2)
elif front1 > front2:
    print(front1, '>', front2)
else:
    print(front1, '=' ,front2)