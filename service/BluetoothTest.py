import socket

print("\n\nperforming inquiry...")

address, services = socket.AF_BLUETOOTH

print("Address: %s" % address)

for name, port in services.items():
     print(u"%s : %d" % (name, port))