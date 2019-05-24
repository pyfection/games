from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.config import Config

from game import Game
from grid import Grid
# import ai.simple


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Button.font_size = 25
Button.markup = True


class Board(GridLayout):
    def __init__(self, grid, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.cols = grid.width
        self.buttons = {}
        self.selected = ()
        self.register_event_type('on_press')
        self.reload()

    def reload(self):
        for button in self.buttons.values():
            self.remove_widget(button)
        self.buttons.clear()
        for x, y in self.grid.keys():
            img_path = 'ux/ship.png' if self.grid.is_ship(x, y) else 'ux/empty.png'
            if self.grid.is_ship(x, y):
                pass
            button = Button(
                on_press=lambda inst, x=x, y=y: self.press(x, y),
                # text=str((x, y)),
                width=64,
                height=64,
                size_hint=(None, None),
                background_normal = img_path,
                background_down = img_path,
                background_disabled_normal = img_path,
                background_disabled_down = img_path,
            )
            self.buttons[(x, y)] = button
            self.add_widget(button)

    def hit(self, x, y, is_ship):
        button = self.buttons[(x, y)]
        button.disabled = True
        if is_ship:
            button.background_disabled_normal = 'ux/sunk.png'
        else:
            button.background_disabled_normal = 'ux/miss.png'

    def press(self, x, y):
        self.selected = (x, y)
        self.dispatch("on_press")

    def on_press(self):
        pass


class LocalPlayer(BoxLayout):
    def __init__(self, player_number, own_grid, **kwargs):
        super().__init__(**kwargs)
        self.player_number = player_number
        self.own_grid = own_grid
        self.enemy_grid = Grid()
        self.current_move = ()
        # self.l_menu = BoxLayout(size_hint_y=None, height=35)
        # self.pred_ai = ai.simple.AI(grid)
        # self.b_reload = Button(text="Reload", on_press=_reload)
        # self.b_predict = Button(text="Predict", on_press=self.predict)
        # self.l_menu.add_widget(self.b_reload)
        # self.l_menu.add_widget(self.b_predict)
        # self.add_widget(self.l_menu)
        self.tracking_grid = Board(self.enemy_grid)
        self.tracking_grid.bind(on_press=self.await_click)
        self.add_widget(self.tracking_grid)
        self.primary_grid = Board(self.own_grid)
        self.primary_grid.disabled = True
        self.add_widget(self.primary_grid)

    def make_move(self):
        self.tracking_grid.disabled = False

    def await_click(self, button):
        self.current_move = self.tracking_grid.selected

    def end_move(self):
        self.tracking_grid.disabled = True
        self.current_move = ()

    def own_hit(self, x, y):
        self.own_grid.hit(x, y)
        self.primary_grid.hit(x, y, self.own_grid.is_ship(x, y))

    def enemy_hit(self, x, y, is_ship):
        self.enemy_grid.hit(x, y, is_ship)
        self.tracking_grid.hit(x, y, is_ship)

    # def predict(self, dt):
    #     x, y = self.pred_ai.predict()

    def uncover_all(self):
        for cell in self.grid.keys():
            if not self.grid.is_covered(*cell):
                continue
            elif self.grid.is_bomb(*cell):
                self.buttons[cell].text = self.BOMB_SYM
            else:
                num = len(self.grid.adjacent_bombs(*cell))
                self.buttons[cell].text = self.NUM_SYMS[num]
            self.uncover(*cell)


class GameApp(App):
    game = Game()

    def build(self):
        local_player = LocalPlayer(0, self.game.world.grids[0])
        self.game.players = (local_player, self.game.players[1])

        self.tick_schedule = Clock.schedule_interval(self.tick, .1)
        return local_player

    def tick(self, dt):
        if self.game.is_over():
            self.tick_schedule.cancel()
            print('Winner:', self.game.current_player)
        else:
            self.game.tick()
