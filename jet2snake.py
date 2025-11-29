import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.core.window import Window
from kivy.uix.label import Label

# --- Setări generale ---
TILE = 20
VIEW_WIDTH = 30  # număr celule vizibile pe lățime
VIEW_HEIGHT = 30 # număr celule vizibile pe înălțime
MAP_SIZE = 100  # pentru demo, 100x100. Schimbă la 1000 pentru labirint real
WIDTH = VIEW_WIDTH * TILE
HEIGHT = VIEW_HEIGHT * TILE
Window.size = (WIDTH, HEIGHT)

# Generare labirint aleatoriu
def generate_maze(size):
    maze = [[random.choice([0,0,0,1]) for _ in range(size)] for _ in range(size)]
    maze[0][0] = 0  # start liber
    maze[size-1][size-1] = 0  # colț opus liber
    return maze

MAZE = generate_maze(MAP_SIZE)

class Ghost:
    COLORS = [(1,0,0), (1,0.5,1), (0,1,1)]  # roșu, roz, cyan
    def __init__(self, x, y, color_index=0):
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 0
        self.color = Ghost.COLORS[color_index % len(Ghost.COLORS)]

    def move(self, maze):
        # simplu: random move dacă zid
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(dirs)
        for dx,dy in dirs:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx]==0:
                self.x, self.y = nx, ny
                break

class PacmanGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.px = 0
        self.py = 0
        self.paused = False

        # puncte
        self.dots = [[(MAZE[r][c]==0) for c in range(MAP_SIZE)] for r in range(MAP_SIZE)]
        self.dots[self.py][self.px] = False

        # fantome
        self.ghosts = [Ghost(MAP_SIZE-2, MAP_SIZE-2, 0), Ghost(MAP_SIZE-2,0,1), Ghost(0,MAP_SIZE-2,2)]

        # tastatură
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_key_down)

        Clock.schedule_interval(self.update, 1/10)

    def _keyboard_closed(self):
        pass

    def on_key_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if key == 'q':
            App.get_running_app().stop()
        elif key == 'escape':
            self.paused = not self.paused
        elif not self.paused:
            if key == 'left':
                self.try_move(-1, 0)
            elif key == 'right':
                self.try_move(1, 0)
            elif key == 'up':
                self.try_move(0, -1)
            elif key == 'down':
                self.try_move(0, 1)
        return True

    def try_move(self, dx, dy):
        nx, ny = self.px + dx, self.py + dy
        if 0 <= nx < MAP_SIZE and 0 <= ny < MAP_SIZE and MAZE[ny][nx]==0:
            self.px, self.py = nx, ny
            if self.dots[ny][nx]:
                self.dots[ny][nx] = False

    def update(self, dt):
        self.canvas.clear()
        # viewport
        start_x = max(0, self.px - VIEW_WIDTH//2)
        start_y = max(0, self.py - VIEW_HEIGHT//2)
        end_x = min(MAP_SIZE, start_x + VIEW_WIDTH)
        end_y = min(MAP_SIZE, start_y + VIEW_HEIGHT)

        with self.canvas:
            # desen labirint și puncte
            for r in range(start_y, end_y):
                for c in range(start_x, end_x):
                    x = (c - start_x) * TILE
                    y = (end_y - r - 1) * TILE
                    if MAZE[r][c]==1:
                        Color(0,0,1)
                        Rectangle(pos=(x,y), size=(TILE,TILE))
                    else:
                        if self.dots[r][c]:
                            Color(1,1,1)
                            Ellipse(pos=(x+TILE*0.3,y+TILE*0.3), size=(TILE*0.4,TILE*0.4))
            # desen Pac-Man
            Color(1,1,0)
            px = (self.px - start_x)*TILE
            py = (end_y - self.py -1)*TILE
            Ellipse(pos=(px,py), size=(TILE,TILE))

            # muta fantomele și le desenează
            for g in self.ghosts:
                if not self.paused:
                    g.move(MAZE)
                gx = (g.x - start_x)*TILE
                gy = (end_y - g.y -1)*TILE
                Color(*g.color)
                Ellipse(pos=(gx,gy), size=(TILE,TILE))
                # coliziune
                if g.x==self.px and g.y==self.py:
                    Color(1,0,0)
                    lbl = Label(text="GAME OVER", font_size=40, pos=(WIDTH/2-100, HEIGHT/2))
                    self.add_widget(lbl)

        if self.paused:
            if not any(isinstance(c,Label) for c in self.children):
                lbl = Label(text="PAUZĂ", font_size=40, pos=(WIDTH/2-50, HEIGHT/2-20))
                self.add_widget(lbl)
        else:
            for c in list(self.children):
                if isinstance(c,Label):
                    self.remove_widget(c)


class PacmanApp(App):
    def build(self):
        return PacmanGame()

if __name__=="__main__":
    PacmanApp().run()

