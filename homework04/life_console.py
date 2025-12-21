import curses
from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border(0)

    def draw_grid(self, screen) -> None:
        for y, row in enumerate(self.life.curr_generation):
            for x, cell in enumerate(row):
                if cell:
                    screen.addch(y + 1, x + 1, "*")
                else:
                    screen.addch(y + 1, x + 1, " ")

    def run(self) -> None:
        curses.wrapper(self._run)

    def _run(self, screen) -> None:
        curses.curs_set(0)
        screen.nodelay(True)

        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()

            self.life.step()

            curses.napms(200)

            key = screen.getch()
            if key == ord('q'):
                break