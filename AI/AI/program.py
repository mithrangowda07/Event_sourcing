x=int(input())
y=int(input())
try:
    print(x/y)
except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")