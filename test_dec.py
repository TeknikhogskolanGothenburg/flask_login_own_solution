from functools import wraps

def dec(arg):
    def decorator(func):
        @wraps(func)
        def wrapper(a, b):
            return arg + func(a, b)
        return wrapper
    return decorator

@dec('hepp')
def something(greeting, name):
    return f'{greeting}, {name}!'



def main():
    print(something.__name__)
    print(something("Hello", "Pelle"))
    print(something("Hi", "Eva"))


if __name__ == '__main__':
    main()
