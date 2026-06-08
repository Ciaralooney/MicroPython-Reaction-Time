import machine
import framebuf
import time
import pyb

MIN_DELAY = 2000
MAX_DELAY = 5000
TIMEOUT   = 3000

i2c  = machine.I2C('X')
fbuf = framebuf.FrameBuffer(bytearray(64*32//8), 64, 32, framebuf.MONO_HLSB)
led  = pyb.LED(1)
sw   = pyb.Switch()

def show(line1, line2=""):
    fbuf.fill(0)
    fbuf.text(line1, 0, 8)
    fbuf.text(line2, 0, 18)
    i2c.writeto(8, fbuf)

def wait_for_release():
    while sw():time.sleep_ms(10)

def rating(ms):
    if ms<200:return "WOW!"
    elif ms<300:return "Great!"
    elif ms<450:return "Good"
    elif ms<600:return "Not bad"
    else:return "Too slow"

def play_round():
    delay_ms = MIN_DELAY+(time.ticks_ms()%(MAX_DELAY-MIN_DELAY))
    show("Wait for it...")
    time.sleep_ms(delay_ms)
    show(">> PRESS NOW!")
    led.on()
    t_start = time.ticks_ms()
    pressed = False
    while time.ticks_diff(time.ticks_ms(), t_start) < TIMEOUT:
        if sw():pressed=True;break
        time.sleep_ms(1)
    t_end = time.ticks_ms()
    led.off()
    if not pressed:return None
    return time.ticks_diff(t_end, t_start)

while True:
    show("Reaction Timer", "Press USR!")
    print("Press USR to start...")
    while not sw():time.sleep_ms(20)
    wait_for_release()
    show("Get ready...", "    3")
    time.sleep(1)
    show("Get ready...", "    2")
    time.sleep(1)
    show("Get ready...", "    1")
    time.sleep(1)
    result = play_round()
    if result is None:
        show("Too slow!", "Try again")
        print("Timed out.")
    else:
        r = rating(result)
        show("{}ms".format(result), r)
        print("{}ms -> {}".format(result, r))
    time.sleep(2)
