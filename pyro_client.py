# import Pyro4

# calculator = Pyro4.Proxy("PYRONAME:calculator")

# result = calculator.add(10, 20)

# print(result)


import Pyro4

uri = input("Enter the server URI")

calculator = Pyro4.Proxy(uri)

a = int(input("Enter number 1: "))
b = int(input("Enter number 2: "))

addition = calculator.add_numbers(a, b)

print(f"Addition {addition}")