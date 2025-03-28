def greet(name):
    return f"Hello, {name}!"

print(greet("John"))


def info(name, age=20, *hobbies, **details):
    print(f"Name: {name}, Age: {age}")
    print(f"Hobbies: {', '.join(hobbies)}")
    print(f"Other details: {details}")

info("Gail", 20, "Soccer", "Reading", city="CDO", country="Philippines")


def add_numbers(*args):
    return sum(args)

print("Sum of the numbers:", add_numbers(5, 10, 15))


def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}:{value}")

show_info(name="Aya", age="15")


def factorial(n):
    if n == 0:
        return 1
    return n*factorial(n-1)

print("Factorial:", factorial(5))


x = 10

def outer():
    y = 20
    def inner():
        z = 30
        print(x,y,z)

    inner()

outer()


def get_coordinates():
    return 10, 20

x,y = get_coordinates()
print(x,y)


def decorator(func):
    def wrapper():
        print("Before function execution")
        func()
        print("After function execution")
    return wrapper

def say_hello():
    print("Hello!")
say_hello = decorator(say_hello)
say_hello()


def outer():
    def inner():
        print("Inner Function")
    return inner

inner_function = outer()
inner_function()


def count_up(n):
    for i in range(n):
        yield i

gen = count_up(3)
print(next(gen))
print(next(gen))
print(next(gen))