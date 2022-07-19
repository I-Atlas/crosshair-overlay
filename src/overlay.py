import tkinter as tk


class CrosshairOverlay(tk.Tk):
    def __init__(self, size=4, width=1, distance=2, color_r=255, color_g=255, color_b=255, is_outline=False,
                 is_center_dot=False, is_crosshair=True, offset_x=0, offset_y=0):
        super().__init__()
        self.l = size
        self.w = width
        self.tn = distance
        self.nk = self._nk(self.w, self.tn)
        self.L = self._L(self.l, self.nk)
        self.LL = self._LL(self.L, self.w)
        self.ox = self.winfo_screenwidth() / 2 - self.LL + offset_x
        self.oy = self.winfo_screenheight() / 2 - self.LL + offset_y
        self.c = "#" + "".join(map(lambda x: format(int(x), "02x"), [color_r, color_g, color_b])).upper()
        self.iol = is_outline
        self.icd = is_center_dot
        self.ich = is_crosshair

        self.geometry(self._gm(self.L + 4, self.L + 4, self.ox, self.oy))
        self.canvas = tk.Canvas(self, bg="snow", width=self.L + self.w, height=self.L + self.w,
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._init_transparent()
        self._create_crosshair_or_dot()

    def _init_transparent(self):
        self.overrideredirect(True)
        self.wm_attributes("-disabled", True)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "snow")

    def _create_crosshair_or_dot(self):
        if self.ich:
            self._create_crosshair()
        if self.icd:
            self._create_center_dot()

    def _create_crosshair(self):
        self._create_crosshair_up()
        self._create_crosshair_down()
        self._create_crosshair_left()
        self._create_crosshair_right()

    def _create_crosshair_up(self):
        if self.iol:
            self.canvas.create_rectangle(self.LL, 0, self.LL + self.w + 1, self.l + 1, fill=self.c)
        else:
            self.canvas.create_rectangle(self.LL, 0, self.LL + self.w + 1, self.l + 1, fill=self.c, outline="snow")

    def _create_crosshair_down(self):
        if self.iol:
            self.canvas.create_rectangle(self.LL, self.l + self.nk, self.LL + self.w + 1, self.L + 1, fill=self.c)
        else:
            self.canvas.create_rectangle(self.LL, self.l + self.nk, self.LL + self.w + 1, self.L + 1, fill=self.c,
                                         outline="snow")

    def _create_crosshair_left(self):
        if self.iol:
            self.canvas.create_rectangle(0, self.LL, self.l + 1, self.LL + self.w + 1, fill=self.c)
        else:
            self.canvas.create_rectangle(0, self.LL, self.l + 1, self.LL + self.w + 1, fill=self.c, outline="snow")

    def _create_crosshair_right(self):
        if self.iol:
            self.canvas.create_rectangle(self.l + self.nk, self.LL, self.L + 1, self.LL + self.w + 1, fill=self.c)
        else:
            self.canvas.create_rectangle(self.l + self.nk, self.LL, self.L + 1, self.LL + self.w + 1, fill=self.c,
                                         outline="snow")

    def _create_center_dot(self):
        if self.iol:
            self.canvas.create_rectangle(self.LL, self.LL, self.LL + self.w + 1, self.LL + self.w + 1, fill=self.c)
        else:
            self.canvas.create_rectangle(self.LL, self.LL, self.LL + self.w + 1, self.LL + self.w + 1, fill=self.c,
                                         outline="snow")

    def _gm(self, ww, wh, offset_x, offset_y):
        return str(int(ww)) + "x" + str(int(wh)) + "+" + str(int(offset_x)) + "+" + str(int(offset_y))

    def _nk(self, w, tn):
        return w + tn * 2

    def _L(self, l, nk):
        return nk + l * 2

    def _LL(self, L, w):
        return (L - w) / 2