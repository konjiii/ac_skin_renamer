from ast import literal_eval

# bla = "print('Hello, World!')"
bla = {"key": "value", "number": 42, "list": [1, 2, 3]}
bla_str = str(bla)


print(bla_str)
print(type(bla_str))

try:
    bla_back = literal_eval(bla_str)
except (ValueError):
    print("HES TRYING TO HACK YOU")
    exit()

if type(bla_back) is not dict:
    raise TypeError("Not a dict after eval!")
print(bla_back)
print(type(bla_back))