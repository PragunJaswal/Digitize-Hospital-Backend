name = "pragun"
new = name.replace("pragun","jaswal")
print(new)

hello = [12,45,47,59,0,12,45]
print(hello.pop())
print(hello)
hello.insert(1,18)
print(hello)
hello.append(472)
print(hello)
print(hello.count(12))
print(hello.index(12))
print(hello.sort(reverse=True))
print(hello)

world = (12,415,150,0,78,58,252,842,45)
print(type(world))
print(world[::-1])
print(world[2:7])
print(world.count(12))
print(world.index(0))

pragun = {"hello":1,"jaswal":2}
print(type(pragun))
print(pragun.keys())
print(pragun.values())
print(pragun.items())
pragun.update({"hello":10})
print(pragun.get("jaswal"))
print(pragun)

pragun.pop("hello")
print(pragun)
pragun.update({"new":89})
print(pragun)
print(len(pragun))
