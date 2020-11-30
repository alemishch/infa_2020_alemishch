import math
import time
import tkinter as tk
from random import randrange as rnd, choice
from PIL import ImageTk, Image

W = 800
H = 600
dH = 45
dW = 60
root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)
canv.focus_set()
num = 0
def change_gun(event):
    global num
    num = (num + 1) % 2
    print(num)

canv.create_line(60, 0, 60, H)
canv.create_line(W - 60, 0, W - 60, H)
canv.create_line(0, H-45, W, H-45)


def playGif(file, b):
    label = tk.Label(canv, image=tk.PhotoImage(file=file))
    frames = []
    i = 1
    n = 5
    while i < n:
        label.place(relx=b.x / W, rely=b.y / H)
        time.sleep(0.7 / n)
        frames.append(tk.PhotoImage(file=file, format=("gif -index {}".format(i))))
        label.configure(image=frames[i - 1])
        i += 1
    label.forget()


class Bomb:
    def __init__(self, x, y, angle):
        self.r = 4
        self.y = y
        self.x = x
        self.v = 4
        self.vx = self.v * math.cos(angle)
        self.vy = self.v * math.sin(angle)
        self.bomb = canv.create_oval(self.x - self.r, self.y + self.r, self.x + self.r, self.y - self.r, fill="yellow")

    def move(self, guns, arr):
        self.x += self.vx
        self.y += self.vy
        canv.coords(self.bomb, self.x - self.r, self.y + self.r, self.x + self.r, self.y - self.r)
        if self.x-self.r>W or self.x+self.r<0 or self.y-self.r>H or self.y+self.r<0:
            canv.delete(self.bomb)
            arr.remove(self)
        for obj in guns:
            if (obj.y - 20 < self.y - self.r and obj.y+40 > self.y + self.r) and self.x - self.r < 60 and\
                    self.x + self.r > 0:
                arr.remove(self)
                canv.delete(self.bomb)
                obj.hp -= 1


class ball():
    def __init__(self, x=40, y=0):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.age = 0
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self, z):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна W*H).
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x - self.r <= 0 or self.x + self.r >= W:
            self.vx *= -1
        if self.y + self.r >= H:
            self.vy *= -0.8
            self.y = H - self.r
            if self.vy < 15:
                self.vy = 15
        self.vy -= 3.4
        self.age += z

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if self.x + self.r >= obj.x - obj.r and self.x - self.r <= obj.x + obj.r and self.y + self.r >= obj.y - obj.r \
                and self.y - self.r <= obj.y + obj.r:
            return True
        else:
            return False

    def destroy(self):
        canv.coords(self.id, -10, -10, -10, 10)
        self.vx, self.vy = 0, 0
        canv.delete(self.id)


class gun():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 5
        self.img = Image.open("ufo.png")
        self.img = self.img.resize((60, 40), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.image = canv.create_image(self.x-20, self.y-20, anchor=tk.NW, image=self.img)
        self.ots = self.x+20
        self.f2_power = 20
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(self.ots, self.y, self.ots + 20, self.y, width=4)

    def switch_weapon(self, event):
        self.weapon_type += 1

    def move(self):
        canv.coords(self.id, self.x+20, self.y, self.x+20 + self.f2_power * math.cos(self.an), self.y +
                    self.f2_power * math.sin(self.an))

    def up(self, event):
        if self.y - 20 > 0:
            self.y -= 5
            canv.move(self.image, 0, -5)
            canv.coords(self.id, self.ots, self.y, self.ots + self.f2_power * math.cos(self.an), self.y +
                        self.f2_power * math.sin(self.an))
            print("")

    def down(self, event):
        if self.y < H - 20:
            self.y += 5
            canv.move(self.image, 0, 5)
            canv.coords(self.id, self.ots, self.y, self.ots + self.f2_power * math.cos(self.an), self.y +
                        self.f2_power * math.sin(self.an))

    def left(self, event):
        if self.x > 0:
            self.x -= 5
            canv.move(self.image, -5, 0)
            canv.coords(self.id, self.x+20, self.y, self.x+20 + self.f2_power * math.cos(self.an), self.y +
                        self.f2_power * math.sin(self.an))

    def right(self, event):
        if self.x < W:
            self.x += 5
            canv.move(self.image, 5, 0)
            canv.coords(self.id, self.x+20, self.y, self.x+20 + self.f2_power * math.cos(self.an), self.y +
                        self.f2_power * math.sin(self.an))

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y - self.y) / (event.x - self.x))
        new_ball.y = self.y + self.f2_power * math.sin(self.an)
        new_ball.x = self.x+20 + self.f2_power * math.cos(self.an)
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 20

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - self.y) / (event.x - self.x))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, self.x+20, self.y,
                    self.x+20 + self.f2_power * math.cos(self.an),
                    self.y + self.f2_power * math.sin(self.an)
                    )
        if self.hp == 0:
            canv.delete(self.id)
            canv.itemconfig(screen1, text="You lost")

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self):
        self.period = rnd(10, 30, 1)
        self.age = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.is_dead = 0
        self.new_target()

    def move(self, z):
        self.x += self.vx
        self.y += self.vy
        if self.y + self.r >= H - dH or self.y - self.r <= 0:
            self.vy *= -1
        if self.x - self.r <= dW or self.x + self.r >= W - dW:
            self.vx *= -1
        self.age += z

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def explode(self, z, arr):
        if not self.is_dead:
            global bombs
            if self.age % self.period < z:
                for i in range(0, 6):
                    an = i * 30
                    bombs += [Bomb(self.x + self.r * math.cos(an), self.y + self.r * math.sin(an), an)]
                self.hit()
                canv.delete(self.id)
                new = target()
                new.new_target()
                arr.append(new)
                arr.remove(self)

    def new_target(self):
        """ Инициализация новой цели. """
        self.xcenter = rnd(200, 780)
        self.ycenter = rnd(50, 550)
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        x = self.x = rnd(230, 700)
        y = self.y = rnd(50, 500)
        r = self.r = rnd(2, 50)
        color = self.color = choice(['blue', 'green', 'red', 'brown'])
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.is_dead = 1


screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun(20, 450)
g2 = gun(300, 580)
text = canv.create_text(100, 20, text="Your health: {}".format(g1.hp))

balls = []


def new_game(event=''):
    global gun, screen1, balls, bombs, num
    guns = [g1, g2]
    enemies, victory = 1, 0
    g1.hp = 5
    balls = []
    bombs = []
    targets = []
    canv.itemconfig(screen1, text='')
    canv.bind('q', change_gun)
    canv.bind('w', g1.up)
    canv.bind('s', g1.down)
    canv.bind('a', g2.left)
    canv.bind('d', g2.right)
    for i in range(1, 5):
        targets.append(target())
    for t in targets:
        t.new_target()
        t.live = 1
    z = 0.03
    while enemies == 1:
        if len(balls):
            guns[num].move()
            for t in targets:
                canv.bind('<Button-1>', guns[num].fire2_start)
                canv.bind('<ButtonRelease-1>', guns[num].fire2_end)
                canv.bind('<Motion>', guns[num].targetting)
                t.move(z)
                t.set_coords()
                t.explode(z, targets)
                canv.itemconfig(text, text="")
                for b in bombs:
                    b.move(guns, bombs)
            for b in balls:
                canv.itemconfig(text, text="Your health: {}".format(guns[num].hp))
                enemies, victory = 0, 1
                b.move(z)
                b.set_coords()
                if b.age > 6:
                    b.destroy
                for t in targets:
                    if b.hittest(t) and t.live:
                        # playGif("gun/gif_explosion.gif", b)
                        b.destroy()
                        balls.remove(b)
                        t.live = 0
                        canv.delete(t.id)
                        t.hit()
                    if (t.live):
                        enemies, victory = 1, 0
            canv.update()
            time.sleep(z)
            guns[num].targetting()
            guns[num].power_up()
        elif not victory:
            for t in targets:
                canv.bind('<Button-1>', guns[num].fire2_start)
                canv.bind('<ButtonRelease-1>', guns[num].fire2_end)
                canv.bind('<Motion>', guns[num].targetting)
                t.move(z)
                t.set_coords()
                canv.itemconfig(text, text="Your health: {}".format(guns[num].hp))
                for b in bombs:
                    b.move(guns, bombs)
                t.explode(z, targets)
            canv.update()
            time.sleep(z)
            guns[num].targetting()
            guns[num].power_up()
    canv.itemconfig(screen1, text='Вы уничтожили все цели')
    for b in balls:
        b.destroy()
        canv.delete(b.id)
        balls.remove(b)
    canv.delete(gun)
    for t in targets:
        canv.delete(t.id)
    root.after(1000, new_game)


new_game()

tk.mainloop()
