#-------------------------------------------------------------------------------
# Name:        neopixel.py
# Purpose:     Simulates NeoPixel
#              Code derived from https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/main/neopixel.py
#              Needs Adafruit PixelBuf -> install it via pip
# Author:
#
# Created:     07.06.2022
# Copyright:   (c)  2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
try:
    import microbit
except ImportError:
    from . import microbit
import adafruit_pixelbuf
import uuid

RGB = "RGB"
GRB = "GRB"
RGBW = "RGBW"
GRBW = "GRBW"


class NeoPixel(adafruit_pixelbuf.PixelBuf):
    _pin: microbit.Pin
    _n: int
    _bpp: int
    _timing: int
    _brightness: float = 1.0
    _auto_write: bool = True
    _pixel_order: str = None
    _variable_name: str = None

    def __init__(self, pin: microbit.Pin, n: int, bpp: int = 3, timing: int = 1, pixel_order: str = None):
        self._pin = pin
        self._n = n
        self._bpp = bpp
        self._timing = timing
        self._pixel_order = pixel_order

        ## generate unique variable name for referencing NeoPixel on micro:bit
        self._variable_name = "np"+uuid.uuid4().hex

        if not self._pixel_order:
            self._pixel_order = GRB if self._bpp == 3 else GRBW
        elif isinstance(self._pixel_order, tuple):
            order_list = [RGBW[order] for order in pixel_order]
            self._pixel_order = "".join(order_list)

        self._pin.parent.cmd("import neopixel")
        self._pin.parent.cmd("%s = neopixel.NeoPixel(%s,%u)" % (self._variable_name, self._pin.name, self._n))
        super().__init__(self._n, brightness=self._brightness, byteorder=self._pixel_order, auto_write=self._auto_write)

    def clear(self):
        try:
            self._pin.parent.cmd("%s.clear()" % self._variable_name)
        except self._pin.parent.repl.repl.REPLException as exc:
            raise MicrobitException(exc.args[0])

    def show(self):
        try:
            for counter in range(0,5):
                self._pin.parent.cmd("%s[%u] = %s" % (self._variable_name, counter, str(self._getitem(counter))))
            self._pin.parent.cmd("%s.show()" % self._variable_name)
        except self._pin.parent.repl.repl.REPLException as exc:
            raise MicrobitException(exc.args[0])
