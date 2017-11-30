from collections import Iterable
from functools import reduce
import time, functools
from time import time, sleep

print('hello,World!')
def test (name,age,**kw):
    print('name:',name,'age:',age,'other:',kw)
test('louis',22,city='hangzhou',work='student')
def move(n, a, b, c):
    if n == 1:
        print(a,'->',c)
    else:
        move(n-1, a, c, b)
        move(1, a, b, c)
        move(n-1, b, a, c)

move(3,'a','b','c')
L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [s.lower() for s in L1 if isinstance(s,str)]
print(L2)
def ms (max):
    n,a,b  = 0,0,1
    while n < max :
        print(b)
        a,b = b,a+b
        n = n+1
    return  'done'
ms(6)



# 生成器和迭代器
def 杨辉三角 ():
    数组1=[]
    数组2=[1,]
    n=0
    while  True:
        yield 数组2
        n=n+1
        if n == 1 :
            数组2=[1,1]
        else:
            数组1=数组2
            临时数组 = [1, 1]
            for x in range(1,n):
                临时数组.insert(x,数组1[x]+数组1[x-1])
                数组2= 临时数组

a = 0
for z in 杨辉三角():
    print(z)
    a = a + 1
    if a == 10:
        break
def triangles():
    L = [1]
    while 1:
        yield L
        L=[1]+[L[i] + L[i+1] for i in range(len(L)-1)]+[1] #生成器的使用

n=0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break



# map练习
def 规范名字(name):
    return name.capitalize()
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(规范名字, L1))
print(L2)

#reduce练习
def 乘积(L):
    def 相乘(x,y):
        return x*y
    return reduce(相乘,L)
print('3 * 5 * 7 * 9 =', 乘积([3, 5, 7, 9]))

#map和reduce共同使用
def float2num(s):
    n=s.index('.')
    def char2num(s):
        return {'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
    def fn(x,y):
        return 10*x+y
    def bn(x,y):
        return 0.1*x+y
    return reduce(fn,map(char2num,s[0:n]))+0.1*reduce(bn,map(char2num,s[:n:-1]))
print('str2float(\'123.456\') =', float2num('123.456'))


# filter函数使用

def is_palindrome(n):
    _str_type = str(n)
    if len(_str_type) == 1:
        return False
    else:
        if _str_type == _str_type[::-1]:
            return True
        else:
            return False

output = filter(is_palindrome, range(1, 1000))
print(list(output))


# 装饰器的使用
start_time=time()
def metric(func):
    @functools.wraps(func)
    def wraps(*args,**kw):
        print('time {0}' .format(time()-start_time))
        return func(*args,**kw)
    return wraps
@metric
def fast(x, y):
    print('我是第一个函数\n')
    time.sleep(0.0012)
    return x + y;

@metric
def slow(x, y, z):
    print('我是第二个函数\n')
    time.sleep(0.1234)
    return x * y * z;

f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')