from machine import Pin, UART, I2C
import ssd1306
import image
from time import sleep as wait

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
led = Pin(25, Pin.OUT)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
btnply = Pin(15, Pin.IN, Pin.PULL_UP)
btnl = Pin(16, Pin.IN, Pin.PULL_UP)
btnr = Pin(17, Pin.IN, Pin.PULL_UP)
btnmode = Pin(18, Pin.IN, Pin.PULL_UP)
currentTrack = 1
volume = 15 #min 0 max 30 default 15
sp_pg = 1 # 1 is vol 2 is place holder
pg = "track"
Ispaused = True
"""
def df_send(cmd, param):
    highByte = (param >> 8) & 0xFF
    lowByte = param & 0xFF
    checksum = 0xFFFF - (0xFF + 0x06 + cmd + 0x00 + highByte + lowByte) + 1
    checksum_high = (checksum >> 8) & 0xFF
    checksum_low = checksum & 0xFF
    
    packet = bytearray([
        0x7E,       # start
        0xFF,       # version
        0x06,       # length
        cmd,        # command
        0x00,       # no feedback
        highByte,   # param high
        lowByte,    # param low
        checksum_high,
        checksum_low,
        0xEF        # end
    ])
    uart.write(packet)
"""
def trackpage(tracknum,music_status):
    #track page
    oled.fill(0) #clear to black
    oled.rect(1, 1, 126, 62, 1) #border
    oled.blit(*image.image_lbits(3, 58)) #left bits
    oled.blit(*image.image_rbits(121, 4)) #right bits
    oled.text("Track no." + str(tracknum), 3, 4, 1)
    if music_status == True:
        oled.text("pause", 4, 15, 1)
    else:
        oled.text("play", 4, 15, 1) #status
    oled.show()

def sppg(volumes):
    oled.fill(0) #clear to black
    oled.rect(1, 1, 126, 62, 1) #border
    oled.blit(*image.image_lbits(3, 58)) #left bits
    oled.blit(*image.image_rbits(121, 4)) #right bits
    oled.blit(*image.vol(53, 14))
    oled.rect(7, 40, 113, 14, 1)
    if volumes == 3:
        oled.fill_rect(9, 42, 10, 10, 1)
    elif volumes == 6:
        oled.fill_rect(9, 42, 10, 10, 1)
        oled.fill_rect(20, 42, 10, 10, 1)
    elif volumes == 9:
        oled.fill_rect(9, 42, 10, 10, 1)
        oled.fill_rect(20, 42, 10, 10, 1)
        oled.fill_rect(31, 42, 10, 10, 1)
    elif volumes == 12:
        oled.fill_rect(9, 42, 10, 10, 1)
        oled.fill_rect(20, 42, 10, 10, 1)
        oled.fill_rect(31, 42, 10, 10, 1)
        oled.fill_rect(42, 42, 10, 10, 1)
    elif volumes == 15:
        oled.fill_rect(9, 42, 10, 10, 1)
        oled.fill_rect(20, 42, 10, 10, 1)
        oled.fill_rect(31, 42, 10, 10, 1)
        oled.fill_rect(42, 42, 10, 10, 1)
        oled.fill_rect(53, 42, 10, 10, 1)
    elif volumes == 18:
        oled.fill_rect(9, 42, 10, 10, 1)
        oled.fill_rect(20, 42, 10, 10, 1)
        oled.fill_rect(31, 42, 10, 10, 1)
        oled.fill_rect(42, 42, 10, 10, 1)
        oled.fill_rect(53, 42, 10, 10, 1)
        oled.fill_rect(64, 42, 10, 10, 1)
    elif volumes == 21:
        oled.fill_rect(9, 42, 10, 10, 1)
        oled.fill_rect(20, 42, 10, 10, 1)
        oled.fill_rect(31, 42, 10, 10, 1)
        oled.fill_rect(42, 42, 10, 10, 1)
        oled.fill_rect(53, 42, 10, 10, 1)
        oled.fill_rect(64, 42, 10, 10, 1)
        oled.fill_rect(75, 42, 10, 10, 1)
    elif volumes == 24:
        oled.fill_rect(9, 42, 10, 10, 1)
        oled.fill_rect(20, 42, 10, 10, 1)
        oled.fill_rect(31, 42, 10, 10, 1)
        oled.fill_rect(42, 42, 10, 10, 1)
        oled.fill_rect(53, 42, 10, 10, 1)
        oled.fill_rect(64, 42, 10, 10, 1)
        oled.fill_rect(75, 42, 10, 10, 1)
        oled.fill_rect(86, 42, 10, 10, 1)
    elif volumes == 27:
        oled.fill_rect(9, 42, 10, 10, 1)
        oled.fill_rect(20, 42, 10, 10, 1)
        oled.fill_rect(31, 42, 10, 10, 1)
        oled.fill_rect(42, 42, 10, 10, 1)
        oled.fill_rect(53, 42, 10, 10, 1)
        oled.fill_rect(64, 42, 10, 10, 1)
        oled.fill_rect(75, 42, 10, 10, 1)
        oled.fill_rect(86, 42, 10, 10, 1)
        oled.fill_rect(97, 42, 10, 10, 1)
    elif volumes == 30:
        oled.fill_rect(9, 42, 10, 10, 1)
        oled.fill_rect(20, 42, 10, 10, 1)
        oled.fill_rect(31, 42, 10, 10, 1)
        oled.fill_rect(42, 42, 10, 10, 1)
        oled.fill_rect(53, 42, 10, 10, 1)
        oled.fill_rect(64, 42, 10, 10, 1)
        oled.fill_rect(75, 42, 10, 10, 1)
        oled.fill_rect(86, 42, 10, 10, 1)
        oled.fill_rect(97, 42, 10, 10, 1)
        oled.fill_rect(108, 42, 10, 10, 1)
    oled.show()


#init lol
oled.fill(0) #clear to black
oled.rect(1, 1, 126, 62, 1) #border
oled.blit(*image.image_lbits(3, 58)) #left bits
oled.blit(*image.image_rbits(121, 4)) #right bits
oled.text("init", 4, 5, 1)
oled.show()

for i in range(1,4):
    led.value(1)
    wait(0.5)
    led.value(0)
    wait(0.5)

while True:
    if pg == "track":
        trackpage(currentTrack, Ispaused)
    elif pg == "sp":
        sppg(volume)
    if currentTrack == 0:
        currentTrack = 1
    if volume > 30:
        volume = 30

    if btnply.value() == 0:
        print("Play pressed")
        if pg == "track":
            if Ispaused:
                Ispaused = False
            elif not Ispaused:
                Ispaused = True
    if btnl.value() == 0:
        print("Left pressed")
        if  pg == "track":
            if currentTrack != 0:
                currentTrack -= 1
        elif pg == "sp":
            volume -= 3
    if btnr.value() == 0:
        print("Right pressed")
        if  pg == "track":
            if currentTrack != 0:
                currentTrack += 1
        elif pg == "sp":
            volume += 3
    if btnmode.value() == 0:
        print("Mode pressed")
        if pg == "track":
            pg = "sp"
        elif pg == "sp":
            pg = "track"
    
