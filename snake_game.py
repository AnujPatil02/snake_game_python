# SNAKE - A simple snake game implemented in Python using Tkinter.

import tkinter as tk, random, json, os
try:
    import winsound; SOUND = True
except ImportError:
    SOUND = False

W, H, CELL, TOP, BZ = 620, 500, 20, 70, 10
HS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")
DIFF = {"Easy": 140, "Medium": 100, "Hard": 65}
C = dict(bg="#0f172a", grid="#1c2b45", bezel="#334155", head="#22d3ee", tail="#0369a1",
          food="#f43f5e", fglow="#fecdd3", bonus="#facc15", bglow="#fff7cc", text="#e2e8f0",
          accent="#facc15", panel="#16213a", shadow="#020617")
DIRS = {"Up": (0, -CELL), "Down": (0, CELL), "Left": (-CELL, 0), "Right": (CELL, 0)}
OPP = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}


def hx(c):  # "#rrggbb" -> (r,g,b)
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def blend(c1, c2, t):
    r1, g1, b1 = hx(c1); r2, g2, b2 = hx(c2)
    return f"#{int(r1+(r2-r1)*t):02x}{int(g1+(g2-g1)*t):02x}{int(b1+(b2-b1)*t):02x}"


def rrect(cv, x1, y1, x2, y2, r=6, **kw):
    pts = [x1+r,y1, x2-r,y1, x2,y1, x2,y1+r, x2,y2-r, x2,y2,
           x2-r,y2, x1+r,y2, x1,y2, x1,y2-r, x1,y1+r, x1,y1]
    return cv.create_polygon(pts, smooth=True, **kw)


def beep(f, d):
    if SOUND:
        try: winsound.Beep(f, d)
        except Exception: pass


class Snake:
    def __init__(self, root):
        self.root = root
        root.title("Snake"); root.resizable(False, False)
        self.cv = tk.Canvas(root, width=W, height=H, bg=C["shadow"], highlightthickness=0)
        self.cv.pack()
        self.high = self.load_hs()
        self.state, self.diff, self.level, self.toast, self.toast_t = "MENU", "Medium", 1, None, 0
        self.speed = DIFF[self.diff]
        self.demo = [(300, 300), (280, 300), (260, 300), (240, 300)]
        self.demo_dir = (CELL, 0)
        root.bind("<Key>", self.on_key)
        self.animate_menu()

    # ---- file I/O ----
    def load_hs(self):
        try:
            with open(HS_FILE) as f: return json.load(f).get("high", 0)
        except Exception: return 0

    def save_hs(self):
        with open(HS_FILE, "w") as f: json.dump({"high": self.high}, f)

    # ---- drawing helpers ----
    def frame(self):
        rrect(self.cv, 2, 2, W-2, H-2, 18, outline=C["bezel"], width=4, fill=C["bg"])

    def grid(self):
        for x in range(BZ, W-BZ, CELL): self.cv.create_line(x, TOP, x, H-BZ, fill=C["grid"])
        for y in range(TOP, H-BZ, CELL): self.cv.create_line(BZ, y, W-BZ, y, fill=C["grid"])

    def stext(self, x, y, txt, font, fill):
        self.cv.create_text(x+2, y+2, text=txt, font=font, fill=C["shadow"])
        self.cv.create_text(x, y, text=txt, font=font, fill=fill)

    def body(self, snake, preview=False):
        n = len(snake)
        for i, (x, y) in enumerate(snake):
            col = C["head"] if i == 0 and not preview else blend(C["head"], C["tail"], i/max(n-1, 1))
            rrect(self.cv, x+1, y+1, x+CELL-1, y+CELL-1, 6, fill=col, outline=C["bg"])
            if i == 0 and not preview: self.eyes(x, y)

    def eyes(self, x, y):
        dx, dy = DIRS[self.dirn]
        cx, cy = x+CELL/2, y+CELL/2
        if dx:
            o = 5 if dx > 0 else -5
            self.cv.create_oval(cx+o-2, cy-5, cx+o+2, cy-1, fill="white")
            self.cv.create_oval(cx+o-2, cy+1, cx+o+2, cy+5, fill="white")
        else:
            o = 5 if dy > 0 else -5
            self.cv.create_oval(cx-5, cy+o-2, cx-1, cy+o+2, fill="white")
            self.cv.create_oval(cx+1, cy+o-2, cx+5, cy+o+2, fill="white")

    # ---- menu ----
    def animate_menu(self):
        if self.state != "MENU": return
        self.draw_menu()
        hxp, hy = self.demo[0]; dx, dy = self.demo_dir; nx, ny = hxp+dx, hy+dy
        if nx > 420: self.demo_dir = (0, CELL); nx, ny = hxp, hy+CELL
        elif ny > 340: self.demo_dir = (-CELL, 0); nx, ny = hxp-CELL, hy
        elif nx < 220 and dy == 0 and dx < 0: self.demo_dir = (0, -CELL); nx, ny = hxp, hy-CELL
        elif ny < 260 and dy < 0: self.demo_dir = (CELL, 0); nx, ny = hxp+CELL, hy
        self.demo.insert(0, (nx, ny)); self.demo.pop()
        self.body(self.demo, preview=True)
        self.root.after(160, self.animate_menu)

    def draw_menu(self):
        self.cv.delete("all"); self.frame(); self.grid()
        self.stext(W//2, 90, "SNAKE", ("Georgia", 38, "bold"), C["accent"])
        self.cv.create_text(W//2, 165, text=f"\U0001F3C6 High Score: {self.high}", font=("Consolas", 14, "bold"), fill=C["text"])
        self.cv.create_text(W//2, 195, text=f"Difficulty: {self.diff}   (press D to change)", font=("Consolas", 12), fill=C["head"])
        self.cv.create_text(W//2, H-60, text="Press ENTER to Start", font=("Consolas", 16, "bold"), fill=C["food"])
        self.cv.create_text(W//2, H-32, text="Arrows = Move | Space = Pause | D = Difficulty | Q = Quit", font=("Consolas", 10), fill=C["text"])

    # ---- input ----
    def on_key(self, e):
        k = e.keysym
        if self.state == "MENU":
            if k == "Return": self.new_game()
            elif k.lower() == "d": self.cycle_diff()
            elif k.lower() == "q": self.root.quit()
        elif self.state == "PLAY":
            if k in DIRS and k != OPP.get(self.dirn): self.next_dir = k
            elif k == "space": self.state = "PAUSE"; self.pause_overlay()
        elif self.state == "PAUSE":
            if k == "space": self.state = "PLAY"; self.cv.delete("pov"); self.tick()
        elif self.state == "OVER":
            if k == "Return": self.new_game()
            elif k.lower() == "m": self.state = "MENU"; self.animate_menu()
            elif k.lower() == "q": self.root.quit()

    def cycle_diff(self):
        names = list(DIFF); self.diff = names[(names.index(self.diff)+1) % len(names)]
        self.speed = DIFF[self.diff]

    # ---- game setup ----
    def new_game(self):
        self.state = "PLAY"
        self.snake = [(190, 190), (170, 190), (150, 190)]
        self.dirn = self.next_dir = "Right"
        self.score, self.level, self.base_speed = 0, 1, self.speed
        self.food = self.rand_food()
        self.bonus, self.bonus_t, self.eaten, self.toast = None, 0, 0, None
        self.tick()

    def rand_food(self, exclude=None):
        cols, rows = (W-2*BZ)//CELL, (H-TOP-BZ)//CELL
        pos = (BZ+random.randint(0, cols-1)*CELL, TOP+random.randint(0, rows-1)*CELL)
        occ = self.snake + ([exclude] if exclude else [])
        return self.rand_food(exclude) if pos in occ else pos

    # ---- game loop ----
    def tick(self):
        if self.state != "PLAY": return
        self.dirn = self.next_dir
        dx, dy = DIRS[self.dirn]
        hxp, hy = self.snake[0]
        nh = (hxp+dx, hy+dy)
        if not (BZ <= nh[0] < W-BZ and TOP <= nh[1] < H-BZ) or nh in self.snake:
            return self.game_over()
        self.snake.insert(0, nh)

        ate = False
        if nh == self.food:
            self.score += 1; self.eaten += 1
            self.food = self.rand_food(self.bonus); ate = True; beep(880, 40)
            if self.eaten % 4 == 0 and not self.bonus:
                self.bonus, self.bonus_t = self.rand_food(self.food), 25
        elif self.bonus and nh == self.bonus:
            self.score += 3; self.bonus = None; ate = True; beep(1200, 60)
        if not ate: self.snake.pop()
        if self.bonus:
            self.bonus_t -= 1
            if self.bonus_t <= 0: self.bonus = None

        lvl = self.score//5 + 1
        if lvl != self.level:
            self.level = lvl
            self.speed = max(45, self.base_speed - (lvl-1)*6)
            self.toast, self.toast_t = f"LEVEL {lvl}!", 8
            beep(660, 80)

        self.render()
        self.root.after(self.speed, self.tick)

    # ---- rendering ----
    def render(self):
        self.cv.delete("all"); self.frame(); self.grid()
        rrect(self.cv, BZ, BZ, W-BZ, TOP-5, 10, fill=C["panel"], outline="")
        self.cv.create_text(100, 38, text=f"Score: {self.score}", font=("Consolas", 14, "bold"), fill=C["accent"])
        self.cv.create_text(W-130, 38, text=f"Best: {self.high}", font=("Consolas", 14, "bold"), fill=C["text"])
        self.cv.create_text(W//2-40, 38, text=f"Lvl {self.level}", font=("Consolas", 13, "bold"), fill=C["head"])
        self.cv.create_text(W//2+60, 38, text=self.diff, font=("Consolas", 11), fill=C["text"])

        fx, fy = self.food
        self.cv.create_oval(fx-2, fy-2, fx+CELL+2, fy+CELL+2, fill=C["fglow"], outline="")
        self.cv.create_oval(fx+2, fy+2, fx+CELL-2, fy+CELL-2, fill=C["food"], outline="")

        if self.bonus:
            bx, by = self.bonus
            p = 4 if self.bonus_t % 2 == 0 else 1
            self.cv.create_oval(bx-p, by-p, bx+CELL+p, by+CELL+p, fill=C["bglow"], outline="")
            self.cv.create_oval(bx+2, by+2, bx+CELL-2, by+CELL-2, fill=C["bonus"], outline="")

        self.body(self.snake)
        if self.toast and self.toast_t > 0:
            self.stext(W//2, TOP+30, self.toast, ("Consolas", 18, "bold"), C["accent"])
            self.toast_t -= 1

    def pause_overlay(self):
        rrect(self.cv, BZ, TOP, W-BZ, H-BZ, 14, fill=C["bg"], stipple="gray50", tags="pov")
        self.cv.create_text(W//2, H//2, text="PAUSED", font=("Georgia", 28, "bold"), fill=C["accent"], tags="pov")
        self.cv.create_text(W//2, H//2+35, text="Press SPACE to resume", font=("Consolas", 12), fill=C["text"], tags="pov")

    def game_over(self):
        self.state = "OVER"; beep(220, 300)
        best = self.score > self.high
        if best: self.high = self.score; self.save_hs()
        self.render()
        rrect(self.cv, BZ, TOP, W-BZ, H-BZ, 14, fill=C["bg"], stipple="gray25")
        self.stext(W//2, H//2-70, "GAME OVER", ("Georgia", 30, "bold"), C["food"])
        self.cv.create_text(W//2, H//2-25, text=f"Score: {self.score}   |   Level: {self.level}", font=("Consolas", 15), fill=C["text"])
        if best:
            self.cv.create_text(W//2, H//2+5, text="\U0001F3C6 New High Score!", font=("Consolas", 14, "bold"), fill=C["accent"])
        self.cv.create_text(W//2, H//2+50, text="ENTER = Restart   M = Menu   Q = Quit", font=("Consolas", 12), fill=C["head"])


if __name__ == "__main__":
    root = tk.Tk()
    Snake(root)
    root.mainloop()
