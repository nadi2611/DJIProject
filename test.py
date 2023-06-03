from pyparrot.Bebop import Bebop
import SimpleHTTPServer, SocketServer
PORT = 8000
httpd = SocketServer.TCPServer(("", PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.allow_reuse_address = True
httpd.serve_forever()

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

#bebop.safe_takeoff(10)
#bebop.smart_sleep(5)
#bebop.safe_land(10)




