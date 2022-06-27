# api.py  01/06/2017  D.J.Whale
#
# an API to a remote micro:bit
#
# TODO: for all pins: digital_write, digital_read
# TODO: for analog pins: analog_write, analog_read
# TODO: lots of other API methods that need implementing.

import time
import math
import uuid
try:
    import repl
except ImportError:
    from . import repl


# NOTE: we have defined MicroBit as a class, so that it is possible later to
# have more than one micro:bit connected, perhaps with independent state
# such as the state of the REPL.

class MicroBit():
    def __init__(self, repl):
        self.repl                 = repl
        self.button_a.parent      = self
        self.button_b.parent      = self
        self.accelerometer.parent = self
        self.display.parent       = self
        self.pin0.parent          = self
        self.pin1.parent          = self
        self.pin2.parent          = self
        self.pin3.parent          = self
        self.pin4.parent          = self
        self.pin5.parent          = self
        self.pin6.parent          = self
        self.pin7.parent          = self
        self.pin8.parent          = self
        self.pin9.parent          = self
        self.pin10.parent         = self
        self.pin11.parent         = self
        self.pin12.parent         = self
        self.pin13.parent         = self
        self.pin14.parent         = self
        self.pin15.parent         = self
        self.pin16.parent         = self
        self.pin19.parent         = self
        self.pin20.parent         = self
        self.pin_logo.parent      = self
        self.radio.parent         = self
        self.audio.parent         = self
        self.music                = self.Music("music", self)
        self.music.parent         = self

    def cmd(self, command):
        ##print("send:%s" % command)
        self.repl.send_command(command)
        r = self.repl.wait_response()
        r = r.strip() # strip last NL from any print statement
        return r

    class Pin():

        NO_PULL: str = "NO_PULL"
        PULL_UP: str = "PULL_UP"
        NO_PULL: str = "NO_PULL"

        def __init__(self, name):
            self.name = name

        def read_digital(self):
            r = self.parent.cmd("print(%s.read_digital())" % self.name)
            r = int(r)
            return r

        def write_digital(self, v):
            try:
                self.parent.cmd("print(%s.write_digital(%s))" % (self.name, str(v)))
            except repl.repl.REPLException as exc:
                raise MicrobitException(exc.args[0])

        def set_pull(self, mode):
            cmd: str = ""
            if isinstance(mode, int):
                cmd = "%s.set_pull(%u)" % (self.name, mode)
            elif isinstance(mode, str):
                cmd = "%s.set_pull(%s.%s)" % (self.name, self.name, mode)
            else:
                cmd = "%s.set_pull(%s)" % (self.name, str(mode))
            try:
                self.parent.cmd(cmd)
            except repl.repl.REPLException as exc:
                raise MicrobitException(exc.args[0])

        def get_pull(self):
            r = self.parent.cmd("print(%s.get_pull())" % self.name)
            r = int(r)
            return r

        def get_mode(self):
            r = self.parent.cmd("print(%s.get_mode())" % self.name)
            return r

        def write_analog(self, v):
            try:
                self.parent.cmd("print(%s.write_analog(%s))" % (self.name, str(v)))
            except repl.repl.REPLException as exc:
                raise MicrobitException(exc.args[0])

        def set_analog_period(self, v):
            try:
                self.parent.cmd("print(%s.set_analog_period(%s))" % (self.name, str(v)))
            except repl.repl.REPLException as exc:
                raise MicrobitException(exc.args[0])

        def set_analog_period_microseconds(self, v):
            try:
                self.parent.cmd("print(%s.set_analog_period_microseconds(%s))" % (self.name, str(v)))
            except repl.repl.REPLException as exc:
                raise MicrobitException(exc.args[0])

    class DigitalPin(Pin):
        def get_analog_period_microseconds(self):
            r = self.parent.cmd("print(%s.get_analog_period_microseconds())" % self.name)
            r = int(r)
            return r

    class AnalogDigitalPin(Pin):
        def read_analog():
            r = self.parent.cmd("print(%s.read_analog())" % self.name)
            r = int(r)
            return r

    class TouchPin(AnalogDigitalPin):
        def is_touched(self):
            r = self.parent.cmd("print(%s.is_touched())" % self.name)
            r = eval(r)
            return r
        def set_touch_mode(self, v):
            try:
                self.parent.cmd("print(%s.set_touch_mode(%s))" % (self.name, str(v)))
            except repl.repl.REPLException as exc:
                raise MicrobitException(exc.args[0])

    class TouchOnlyPin():
        def __init__(self, name):
            self.name = name
        def is_touched(self):
            r = self.parent.cmd("print(%s.is_touched())" % self.name)
            r = eval(r)
            return r
        def set_touch_mode(self, v):
            try:
                self.parent.cmd("print(%s.set_touch_mode(%s))" % (self.name, str(v)))
            except repl.repl.REPLException as exc:
                raise MicrobitException(exc.args[0])

##    class AnalogDigitalPin():
##        def __init__(self, name):
##            self.name = name
##
##        def is_touched(self):
##            r = self.parent.cmd("print(%s.is_touched())" % self.name)
##            r = eval(r)
##            return r
##
##    class DigitalPin():
##        def __init__(self, name):
##            self.name = name
##
##        def is_touched(self):
##            r = self.parent.cmd("print(%s.is_touched())" % self.name)
##            r = eval(r)
##            return r

    class Button():
        def __init__(self, name):
            self.name = name

        def was_pressed(self):
            r = self.parent.cmd("print(%s.was_pressed())" % self.name)
            r = eval(r)
            return r

        def is_pressed(self):
            r = self.parent.cmd("print(%s.is_pressed())" % self.name)
            r = eval(r)
            return r

    class Accelerometer():
        def __init__(self, name):
            self.name = name

        def get_x(self):
            r = self.parent.cmd("print(%s.get_x())" % self.name)
            r = int(r)
            return r

        def get_y(self):
            r = self.parent.cmd("print(%s.get_y())" % self.name)
            r = int(r)
            return r

        def get_z(self):
            r = self.parent.cmd("print(%s.get_z())" % self.name)
            r = int(r)
            return r

        def get_values(self):
            r = self.parent.cmd("print(%s.get_values())" % self.name)
            r = r[1:-1] # remove brackets
            r = r.split(",")
            r = (int(r[0]), int(r[1]), int(r[2]))
            return r

        def get_strength(self):
            r = self.parent.cmd("print(%s.get_strength())" % self.name)
            r = int(r)
            return r

        def current_gesture(self):
            r = self.parent.cmd("print(%s.current_gesture())" % self.name)
            return r

        def is_gesture(self):
            r = self.parent.cmd("print(%s.is_gesture())" % self.name)
            r = eval(r)
            return r

        def was_gesture(self):
            r = self.parent.cmd("print(%s.was_gesture())" % self.name)
            r = eval(r)
            return r

        def get_gestures(self):
            r = self.parent.cmd("print(%s.get_gestures())" % self.name)
            r = r[1:-1] # remove brackets
            gestures = ()
            if r != '':
                r = r.split(",")
                for g in r:
                    g=g.strip()
                    g=g[1:-1]
                    gestures = (*gestures, g)
            return gestures

        def set_range(self, v):
            try:
                self.parent.cmd("%s.set_range(%s))" % (self.name, str(v)))
            except repl.repl.REPLException as exc:
                raise MicrobitException(exc.args[0])

    class StandardImage():
        def __init__(self, name):
            self.name = name

    class Image():
        STD_IMAGE_NAMES = [
            "HEART", "HEART_SMALL", "HAPPY", "SMILE", "SAD", "CONFUSED", "ANGRY", "ASLEEP", "SURPRISED",
            "SILLY", "FABULOUS", "MEH", "YES", "NO", "TRIANGLE", "TRIANGLE_LEFT", "CHESSBOARD",
            "DIAMOND", "DIAMOND_SMALL", "SQUARE", "SQUARE_SMALL", "RABBIT", "COW",
            "MUSIC_CROTCHET", "MUSIC_QUAVER", "MUSIC_QUAVERS", "PITCHFORK", "XMAS", "PACMAN",
            "TARGET", "TSHIRT", "ROLLERSKATE", "DUCK", "HOUSE", "TORTOISE", "BUTTERFLY", "STICKFIGURE",
            "GHOST", "SWORD", "GIRAFFE", "SKULL", "UMBRELLA", "SNAKE",
            "CLOCK12","CLOCK11","CLOCK10","CLOCK9","CLOCK8","CLOCK7","CLOCK6","CLOCK5",
            "CLOCK4","CLOCK3","CLOCK2","CLOCK1",
            "ARROW_N", "ARROW_NE","ARROW_E","ARROW_SE","ARROW_S","ARROW_SW","ARROW_W","ARROW_NW"
        ]
        STD_IMAGES = []
        ##ALL_CLOCKS = []
        ##ALL_ARROWS = []

        def __init__(self, bitmap_str):
            self.bitmap_str = bitmap_str

        def __str__(self):
            return self.bitmap_str

    class Radio():
        def __init__(self, name):
            self.name = name

        def on(self):
            self.parent.cmd("import radio")
            self.parent.cmd("%s.on()" % (self.name))

        def config(self, **kwargs):
            self.parent.cmd("import radio")
            kwargs_str = ', '.join('%s=%r' % x for x in kwargs.items())
            ##print(kwargs_str)
            self.parent.cmd("%s.config(%s)" % (self.name, kwargs_str))

        def off(self):
            self.parent.cmd("%s.off()" % (self.name))

        def send(self, message):
            self.parent.cmd("%s.send(\"%s\")" % (self.name, message))

        def receive(self):
            #TODO: may need to add better handling of None somehow?
            return self.parent.cmd("print(%s.receive())" % (self.name))

        def receive_bytes(self):
            data = self.parent.cmd("print(%s.receive_bytes())" % (self.name))
            #TODO: may need to add better handling of None somehow?
            return data

        def reset(self):
            self.parent.cmd("%s.reset()" % (self.name))

    class Display():
        def __init__(self, name):
            self.name = name

        def scroll(self, s):
            if not isinstance(s, str):
                raise RuntimeError("display.scroll needs a str")
            self.parent.cmd("%s.scroll(\"%s\")" % (self.name, s))

        def show(self, v):
            if isinstance(v, MicroBit.StandardImage):
                self.parent.cmd("%s.show(Image.%s)" % (self.name, v.name))

            elif isinstance(v, MicroBit.Image):
                s = v.__str__() # get bitmap
                self.parent.cmd("%s.show(Image(\"%s\"))" % (self.name, s))

            elif isinstance(v, str):
                self.parent.cmd("%s.show(\"%s\")" % (self.name, v))

            elif isinstance(v, int):
                if v >= 0 and v <= 99:
                    import font2x5
                    istr = font2x5.build_image_string(v)
                    self.parent.cmd("%s.show(Image(\"%s\"))" % (self.name, istr))
                else:
                    v = str(v)
                    self.parent.cmd("%s.show(\"%s\")" % (self.name, v))
            elif isinstance(v, list):
                #TODO: This is really an iterable.
                #but it is most likely a list of images such as ALL_CLOCKS
                raise RuntimeError("List parameters not yet implemented for Display.show()")

        def clear(self):
            self.parent.cmd("%s.clear()" % self.name)

        def set_pixel(self, x : int, y : int, b : int):
            self.parent.cmd("%s.set_pixel(%s, %s, %s)" % (self.name, x, y, b))

        def get_pixel(self, x : int, y : int):
            b = self.parent.cmd("print(%s.get_pixel(%s, %s))" % (self.name, x, y))
            b = int(b)
            if (b == 0):
                return 0
            if (b == 255):
                return 9
            else:
                return (int)(math.log(b,2) + 1)

        def on(self):
            self.parent.cmd("%s.on()" % self.name)

        def off(self):
            self.parent.cmd("%s.off()" % self.name)

        def is_on(self):
            r = self.parent.cmd("print(%s.is_on())" % self.name)
            r = eval(r)
            return r

        def read_light_level(self):
            r = self.parent.cmd("print(%s.read_light_level())" % self.name)
            r = int(r)
            return r

    class Audio():
        def __init__(self, name):
            self.name = name

        def play(self, source, wait = True, pin = None, return_pin = None):
            if pin == None:
                pin = self.parent.pin0
            if isinstance(source, str):
                self.parent.cmd("%s.play(%s)" % (self.name, source))
##  Playing iterations of AudioFrames is not usefull in slave mode of microbit
##            elif isinstance(source, AudioFrame):
##                variable_name = "af"+uuid.uuid4().hex
##                self.parent.cmd("%s = audio.AudioFrame()" % variable_name)
##                for i in range(0, len(source))
##                    self.parent.cmd("%s[%u] = %u" % (variable_name, i, source[i])
##                self.parent.cmd("%s.play(%s)" % (self.name, variable_name))

        class AudioFrame(list):
            def __init__(self, *args):
                super().__init__(*args)
                for i in range(0,32):
                    super().append(128)

    class Sound():
        GIGGLE: str = "Sound.GIGGLE"
        HAPPY: str = "Sound.HAPPY"
        HELLO: str = "Sound.HELLO"
        MYSTERIOUS: str = "Sound.MYSTERIOUS"
        SAD: str = "Sound.SAD"
        SLIDE: str = "Sound.SLIDE"
        SOARING: str = "Sound.SOARING"
        SPRING: str = "Sound.SPRING"
        TWINKLE: str = "Sound.TWINKLE"
        YAWN: str = "Sound.YAWN"

    class Music():
        def __init__(self, name, parent = None):
            self.name = name
            self.parent = parent
            parent.cmd("import %s" % self.name)

        def set_tempo(self, ticks = 4, bpm = 120):
            try:
                self.parent.cmd("%s.set_tempo(%u, %u)" % (self.name, ticks, bpm))
            except repl.repl.REPLException as exc:
                raise MicrobitException(exc.args[0])

        def get_tempo(self):
            r = self.parent.cmd("print(%s.get_tempo())" % self.name)
            r = r[1:-1]
            r = r.split(",")
            r = (int(r[0]), int(r[1]))
            return r

        def play(self, music, pin = None, wait = True, loop = False):
            if pin == None:
                pin = self.parent.pin0
            if isinstance(music, str):
                music = [music]
            if isinstance(music, list):
                self.parent.cmd("%s.play(%s, %s, %s, %s)" % (self.name, str(music), pin.name, str(wait), str(loop)))

    def sleep(self, ms):
        time.sleep(float(ms)/1000)

    def temperature(self):
        r = self.cmd("print(temperature())")
        r = int(r)
        return r


    button_a      = Button('button_a')
    button_b      = Button('button_b')
    accelerometer = Accelerometer("accelerometer")
    display       = Display("display")
    pin0          = TouchPin("pin0")
    pin1          = TouchPin("pin1")
    pin2          = TouchPin("pin2")
    pin3          = AnalogDigitalPin("pin3")
    pin4          = AnalogDigitalPin("pin4")
    pin5          = DigitalPin("pin5")
    pin6          = DigitalPin("pin6")
    pin7          = DigitalPin("pin7")
    pin8          = DigitalPin("pin8")
    pin9          = DigitalPin("pin9")
    pin10         = AnalogDigitalPin("pin10")
    pin11         = DigitalPin("pin11")
    pin12         = DigitalPin("pin12")
    pin13         = DigitalPin("pin13")
    pin14         = DigitalPin("pin14")
    pin15         = DigitalPin("pin15")
    pin16         = DigitalPin("pin16")
    pin19         = DigitalPin("pin19")
    pin20         = DigitalPin("pin20")
    pin21         = DigitalPin("pin21")
    pin_logo      = TouchOnlyPin("pin_logo")
    radio         = Radio("radio")
    audio         = Audio("audio")
    ##music         = Music(self, "music")

    # Dynamically build attributes in Image for every standard image
    for image_name in Image.STD_IMAGE_NAMES:
        i = StandardImage(image_name)
        setattr(Image, image_name, i)
        Image.STD_IMAGES.append(i)

    # Dynamically build Image.ALL_CLOCKS now Image.CLOCK* is defined
    Image.ALL_CLOCKS = [
        Image.CLOCK12, Image.CLOCK1, Image.CLOCK2, Image.CLOCK3, Image.CLOCK4, Image.CLOCK5,
        Image.CLOCK6, Image.CLOCK7, Image.CLOCK8, Image.CLOCK9, Image.CLOCK10, Image.CLOCK11
    ]

    # Dynamically build Image.ALL_ARROWS
    Image.ALL_ARROWS = [
        Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E, Image.ARROW_SE,
        Image.ARROW_S, Image.ARROW_SW, Image.ARROW_W, Image.ARROW_NW
    ]

## This class converts REPLExceptions
class MicrobitException(Exception):
    def __init__(self, msg=None):
        if msg[-2:]=="\r\n":
            msg=msg[0:-2]
            msg = msg[msg.rindex("\n"):]
        Exception.__init__(self, msg)


# END
