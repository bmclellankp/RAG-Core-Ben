# app.py

def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def factorial(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def main():
    name = "Alice"
    print(greet(name))
    
    x, y = 5, 7
    print(f"The sum of {x} and {y} is {add(x, y)}")
    
    num = 5
    print(f"The factorial of {num} is {factorial(num)}")
    
    fib_num = 10
    print(f"The {fib_num}th Fibonacci number is {fibonacci(fib_num)}")

if __name__ == "__main__":
    main()
