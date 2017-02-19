import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import matplotlib.pyplot as plt
import numpy as np

print('===Initialized===\n')


# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))



## Another way to do realtime plot
# x = np.linspace(0, 6*np.pi, 100)
# y = np.sin(x)

# You probably won't need this if you're embedding things in a tkinter plot...
# plt.ion()

# fig = plt.figure()
# ax = fig.add_subplot(111)
# line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

# for phase in np.linspace(0, 10*np.pi, 500):
#     line1.set_ydata(np.sin(x + phase))
#     fig.canvas.draw()
#     time.sleep(.1)


# import random #probably unneeded
from collections import deque


# simulates input from serial port
# def random_gen():
#     while True:
#         val = random.randint(1,10)
#         yield val
#         time.sleep(0.05)


a1 = deque([0]*100) #a1 is plotted variable, long que

ax = plt.axes(xlim=(0, 20), ylim=(0, 1000)) #can change to accomondate pdata
plt.xlabel('Time [.5s step]')
plt.ylabel('Pressure Reading(Psig)')
plt.grid(1,which='both',axis='both')
plt.title('Realtime Pressure Reading(ch0)')
d = mcp.read_adc(0)

#conversion from adc vals to psi, note calibration factor and datasheet

line, = plt.plot(a1)
plt.ion()
plt.ylim([0,150])
plt.show()

for i in range(0,20000):
    d = mcp.read_adc(0)
    dv = d *4.5 / 1023 #Scale ADC ticks to Voltage
    dp = .1599*d - 16.506 #Scale ticks to Pressure 
    print "ADC Clicks: %6d  Voltage(4.5 Vref): %6.3f  Pressure(Psig): %6.2f" % (d,dv,dp)
    a1.appendleft(dp)
    datatoplot = a1.pop()
    line.set_ydata(a1)
    plt.draw()
    # print a1 #also print pressure data and modified
    i += 1
    time.sleep(0.15)
    plt.pause(0.0001)   

