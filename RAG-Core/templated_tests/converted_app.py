# app.py

def greet(name):
    return u"Hello, {0}!".format(name)

def add(a, b):
    return a + b

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def fibonacci(n):
    a, b = 0, 1
    for _ in xrange(n):
        a, b = b, a + b
    return a

def main():
    name = u"Alice"
    print greet(name)
    
    x, y = 5, 7
    print u"The sum of {0} and {1} is {2}".format(x, y, add(x, y))
    
    num = 5
    print u"The factorial of {0} is {1}".format(num, factorial(num))
    
    fib_num = 10
    print u"The {0}th Fibonacci number is {1}".format(fib_num, fibonacci(fib_num))

if __name__ == "__main__":
    main()