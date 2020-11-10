from random import randrange as rnd, choice
import tkinter as tk
import math
import time
# print (dir(math))

W = 800
H = 600
dH = 0
dW = 0
root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


def playGif(file, b):
    label = tk.Label(canv, image=tk.PhotoImage(file = file))
    frames = []
    i = 1
    n = 5
    while i < n:
        label.place(relx=b.x/W, rely=b.y/H)
        time.sleep(0.7 / n)
        frames.append(tk.PhotoImage(file=file, format=("gif -index {}".format(i))))
        label.configure(image = frames[i-1])
        i += 1
    label.forget()
class ball():
    def __init__(self, x=40, y=450):
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

    def destroy(self):
        self.x, self.y, self.vx, self.vy, r = 0, 0, 0, 0, 0
        self.set_coords()
        canv.delete(self.id)

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


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self, points):
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.y + self.r >= H - dH or self.y - self.r <= dH:
            self.vy *= -1
        if self.x - self.r <= dW or self.x + self.r >= W - dW:
            self.vx *= -1

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def new_target(self):
        """ Инициализация новой цели. """
        self.xcenter = rnd(200,780)
        self.ycenter = rnd(50, 550)
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        x = self.x = rnd(200, 780)
        y = self.y = rnd(50, 550)
        r = self.r = rnd(2, 50)
        color = self.color = choice(['blue', 'green', 'red', 'brown'])
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)

screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []

def new_game(event=''):
    global gun, screen1, balls, bullet
    points = 0
    id_points = canv.create_text(30, 30, text=points, font='28')
    enemies, victory = 1, 0
    bullet = 0
    balls = []
    targets = []
    canv.itemconfig(screen1, text='')
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    for i in range(1, 5):
        targets.append(target(0))
    for t in targets:
        t.new_target()
        t.live = 1
    z = 0.03
    while enemies == 1:
        if len(balls)>0:
            for t in targets:
                t.move()
                t.set_coords()
            for b in balls:
                enemies, victory = 0, 1
                b.move(z)
                b.set_coords()
                if b.age > 6:
                    b.destroy()
                for t in targets:
                    if b.hittest(t) and t.live:
                        #playGif("gun/gif_explosion.gif", b)
                        b.destroy()
                        t.live = 0
                        canv.delete(t.id)
                        points += 1
                        t.hit()
                    if(t.live):
                        enemies, victory = 1, 0
            canv.update()
            time.sleep(z)
            canv.itemconfig(id_points, text=points)
            g1.targetting()
            g1.power_up()
        elif not victory:
            for t in targets:
                t.move()
                t.set_coords()
            canv.itemconfig(id_points, text=points)
            canv.update()
            time.sleep(z)
            g1.targetting()
            g1.power_up()
    canv.itemconfig(screen1, text='Вы уничтожили все цели за ' + str(bullet) + ' выстрелов')
    canv.delete(gun)
    for t in targets:
        canv.delete(t.id)
    root.after(1000, new_game)


new_game()

tk.mainloop()