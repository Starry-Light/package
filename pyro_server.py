# import Pyro4

# @Pyro4.expose
# class Calculator:

#     def add(self, a, b):
#         return a + b

# daemon = Pyro4.Daemon()

# ns = Pyro4.locateNS()

# uri = daemon.register(Calculator)

# ns.register("calculator", uri)

# daemon.requestLoop()


import Pyro4

@Pyro4.expose
class Calculator:
    def add_numbers(self, a, b):
        return a + b

daemon = Pyro4.Daemon()

uri = daemon.register(Calculator())

print("Server running")
print("URI: ", uri)

daemon.requestLoop()