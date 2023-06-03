from pyparrot.Bebop import Bebop

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

#bebop.safe_takeoff(10)
#bebop.smart_sleep(5)
#bebop.safe_land(10)




