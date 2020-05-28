def funcz():
    print("funcz")


a = [("x", "y"), ("x1", "y1", funcz)]

res = [(x, y, z) for x, y, *z in a]


print(res)
