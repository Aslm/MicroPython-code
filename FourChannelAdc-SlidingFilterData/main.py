# main.py -- put your code here!
import pyb
import time
import array
#
from pyb import UART
from pyb import LED
from pyb import Switch
from pyb import Timer
from pyb import ADC
from pyb import Pin
#
from fifter.SlideAvg import SlideAvg


def deDug(data, flag=True):
    """ """
    if flag:
        print("DEBUG--> " + str(data))
    else:
        pass


def runLedStartNoBlock(flag=True, tim_num=14, tim_freq=0.3, led_num=4):
    """ """
    if flag:
        tim = Timer(tim_num, freq=tim_freq)
        tim.callback(lambda cb_fun: LED(led_num).toggle())
    else:
        pass


if __name__ == "__main__":

    deDug(str(pyb.freq()))
    deDug('CODE START -->\n')
    # runLedStartNoBlock(flag=True)

    #
    uart = UART(6, 115200)
    uart.write('--> CODE START -->\n')
    #
    adc = [ADC(Pin('X8'))] * 4
    adc[0] = ADC(Pin('X8'))
    adc[1] = ADC(Pin('X7'))
    adc[2] = ADC(Pin('X6'))
    adc[3] = ADC(Pin('X5'))

    #
    f_win_n = 10
    f_data = [(array.array('i', [0] * (3 + f_win_n))) for i in range(4)]

    f_data[0][0] = len(f_data[0])
    f_data[1][0] = len(f_data[1])
    f_data[2][0] = len(f_data[2])
    f_data[3][0] = len(f_data[3])

    tim_x = 0
    while True:
        tim_x += 1
        if tim_x > 10000:
            tim_x = 0

        time.sleep_ms(1)

        adc_val = [0] * 4
        dif = [0] * 2

        adc_val[0] = SlideAvg(f_data[0], adc[0].read())
        adc_val[1] = SlideAvg(f_data[1], adc[1].read())
        adc_val[2] = SlideAvg(f_data[2], adc[2].read())
        adc_val[3] = SlideAvg(f_data[3], adc[3].read())

        dif[0] = adc_val[0] - adc_val[1]
        dif[1] = adc_val[2] - adc_val[3]

        par = [[100, -50], [250, -50]]
        if (dif[0] <= par[0][0] and dif[0] >= par[0][1]) and (dif[0] <= par[1][0] and dif[0] >= par[0][1]):
            LED(1).off()
            LED(2).on()
            LED(3).off()
        elif dif[0] > par[0][0] and dif[1] > par[1][0]:
            LED(1).off()
            LED(2).off()
            LED(3).on()
        elif dif[0] < par[0][1] and dif[1] < par[1][1]:
            LED(1).on()
            LED(2).off()
            LED(3).off()


        if tim_x % 500 == 0:
            deDug('ADC -> %d | %d | %d | %d |***| %d | %d' %
                  (adc_val[0], adc_val[1], adc_val[2], adc_val[3], dif[0], dif[1]),
                  flag=True)
            # uart.write(val_str + '\n')

# '''''''''''''''''''''''''''''''''''''''
# led3 = pyb.LED(3)
# led3.intensity(100)
# led3.toggle()
