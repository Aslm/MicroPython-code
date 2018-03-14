# main.py -- put your code here!
from pyb import UART

u1 = UART(6, 115200)#Y1-->TX | Y2-->RX
u1.write('START!!!\n')
data = bytearray([1,2,3])
u1.write(data)

