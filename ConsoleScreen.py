import logging
import os
import time

class ConsoleScreen:

    def __init__(self, dimensions=(948, 506), fontSize=2):
        changeFontSize(fontSize)

        self.width, self.height = dimensions
        os.system(f'mode con: cols={self.width+4} lines={self.height+4}')
        self.background = " "
        self.shade = {
            "light": u"\u2591",
            "medium": u"\u2592",
            "dark": u"\u2593",
            "full": u"\u2588",
            "X": "X",
            "x": "x"
        }
        self.bigPixelShades = getBigPixelShades()
        self.pixel = self.shade["full"]

        self.field = [[self.background for x in range(self.width)] for y in range(self.height)]
        logging.basicConfig(filename='ConsoleScreen.log', level=logging.INFO, filemode='w')

    def clearField(self):
        self.field = [[self.background for x in range(self.width)] for y in range(self.height)]

    def clearScreen(self):
        os.system('cls')

    def clear(self):
        self.clearScreen()
        self.clearField()

    def roundPoint(self, p, r=0):
        return tuple([int(round(x, r)) for x in p])

    def mapFunc(self, value, start1, stop1, start2,
                stop2):  # Maps a value from a range ont another value from a different range
        return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

    def getShade(self, value):
        return [" ", u"\u2591", u"\u2592", u"\u2593", u"\u2588"][
            round(self.mapFunc(value, 255, 0, 0, 4))]

    def getBigPixelShade(self, value=255):
        num = round(self.mapFunc(value, 0, 255, 0, 16))
        return self.bigPixelShades[num]

    def onScreen(self, pixel):
        if 0 < pixel[0] < self.width and 0 < pixel[1] < self.height:
            return True
        return False

    def drawPixel(self, xy, shade=u"\u2588"):
        if self.onScreen(xy):
            self._drawPixel(xy, shade)

    def _drawPixel(self, xy, shade=u"\u2588"):
        x, y = xy
        self.field[round(y)][round(x)] = shade

    def drawBigPixel(self, xy, value=100):
        x, y = xy
        shades = self.getBigPixelShade(value)
        points = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
        for p, s in zip(points, shades):
            if self.onScreen(p):
                self.drawPixel(p, s)

    def drawLine(self, p1, p2, shade=u"\u2588", draw=True):
        p1 = self.roundPoint(p1)
        p2 = self.roundPoint(p2)

        x0, y0 = p1
        x1, y1 = p2

        line = []

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                line.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                line.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        line.append((x, y))

        line = list(set(line))
        if draw:
            for c in line:
                self.drawPixel(c, shade)
        return line

    def drawTriangle(self, triangle, fill=False, shade=u"\u2588"):
        l1 = self.drawLine(triangle[0], triangle[1], shade)
        l2 = self.drawLine(triangle[1], triangle[2], shade)
        l3 = self.drawLine(triangle[2], triangle[0], shade)

    def drawCircle(self, xy, r, shade=False, draw=True):  # Draws circle with radius "r" from midpoint "xy".
        xc, yc = xy
        coords = []

        def drawC(xc, yc, x, y):
            coords.append((xc + x, yc + y))
            coords.append((xc - x, yc + y))
            coords.append((xc + x, yc - y))
            coords.append((xc - x, yc - y))
            coords.append((xc + y, yc + x))
            coords.append((xc - y, yc + x))
            coords.append((xc + y, yc - x))
            coords.append((xc - y, yc - x))

        x = 0
        y = r
        d = 3 - 2 * r
        drawC(xc, yc, x, y)
        while y >= x:
            x += 1
            if (d > 0):
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            drawC(xc, yc, x, y)
            # drawC(xc, yc, zc, x+1, y)
            # drawC(xc, yc, zc, x-1, y)

        if draw:
            for c in coords:
                self.drawPixel(c, shade=shade)
        return coords

    def display(self, border=False):
        try:
            if border:
                filledLines = "".join([border for n in range(self.width + 2)])
                everythingElse = "\n".join([border + "".join(self.field[n]) + border for n in range(len(self.field))])
                print(filledLines + "\n" + everythingElse + "\n" + filledLines)
            else:
                print("\n".join(["".join(r) for r in self.field]))
        except Exception as e:
            logging.error("Failed Printing Field")
            logging.error(str(e))



def getBigPixelShades():
    s = [" ", u"\u2591", u"\u2592", u"\u2593", u"\u2588"]
    return [[s[0], s[0], s[0], s[0]],
            [s[1], s[0], s[0], s[0]],
            [s[1], s[1], s[0], s[0]],
            [s[1], s[1], s[1], s[0]],
            [s[1], s[1], s[1], s[1]],

            [s[2], s[1], s[1], s[1]],
            [s[2], s[2], s[1], s[1]],
            [s[2], s[2], s[2], s[1]],
            [s[2], s[2], s[2], s[2]],

            [s[3], s[2], s[2], s[2]],
            [s[3], s[3], s[2], s[2]],
            [s[3], s[3], s[3], s[2]],
            [s[3], s[3], s[3], s[3]],

            [s[4], s[3], s[3], s[3]],
            [s[4], s[4], s[3], s[3]],
            [s[4], s[4], s[4], s[3]],
            [s[4], s[4], s[4], s[4]],
            ]


def changeFontSize(size=2):
    from ctypes import POINTER, WinDLL, Structure, sizeof, byref
    from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(Structure):
        _fields_ = [
            ("X", SHORT),
            ("Y", SHORT),
        ]

    class CONSOLE_FONT_INFOEX(Structure):
        _fields_ = [
            ("cbSize", ULONG),
            ("nFont", DWORD),
            ("dwFontSize", COORD),
            ("FontFamily", UINT),
            ("FontWeight", UINT),
            ("FaceName", WCHAR * LF_FACESIZE)
        ]

    kernel32_dll = WinDLL("kernel32.dll")

    get_last_error_func = kernel32_dll.GetLastError
    get_last_error_func.argtypes = []
    get_last_error_func.restype = DWORD

    get_std_handle_func = kernel32_dll.GetStdHandle
    get_std_handle_func.argtypes = [DWORD]
    get_std_handle_func.restype = HANDLE

    get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
    get_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
    get_current_console_font_ex_func.restype = BOOL

    set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
    set_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
    set_current_console_font_ex_func.restype = BOOL

    stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = sizeof(CONSOLE_FONT_INFOEX)

    font.dwFontSize.X = size
    font.dwFontSize.Y = size

    set_current_console_font_ex_func(stdout, False, byref(font))


if __name__ == "__main__":
    f = ConsoleScreen()
    t = time.time()
    f.drawTriangle(((40, 6), (300, 50), (3, 120)), fill=False)
    print(time.time()-t)
    # f.drawLine((0, 0), (948, 506))
    #f.drawBigPixel((10, 10), 30)
    #f.display(f.shade["full"])
    input("[DONE!]")
