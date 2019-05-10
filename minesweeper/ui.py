from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.config import Config

from grid import Grid
import ai.simple


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Button.font_name = "unifont-12.0.01.ttf"
Button.font_size = 25
Button.markup = True


class GridUI(GridLayout):
    BOMB_SYM = '[color=000000]\u2BBF[/color]'
    FLAG_SYM = '\u2691'
    NUM_SYMS = [
        '',
        '[color=0b24fb]1[/color]',
        '[color=0e7a11]2[/color]',
        '[color=fc0d1b]3[/color]',
        '[color=020b79]4[/color]',
        '[color=790207]5[/color]',
        '[color=087f7f]6[/color]',
        '[color=111211]7[/color]',
        '[color=808080]8[/color]',
    ]

    def __init__(self, bomb_count, width, height, **kwargs):
        super().__init__(**kwargs)
        self.bomb_count = bomb_count
        self.width = width
        self.height = height
        self.buttons = {}
        self.grid = Grid(bomb_count, width, height)
        self.cols = width
        self.reload()


    def reload(self):
        self.grid.reset()
        for button in self.buttons.values():
            self.remove_widget(button)
        self.buttons.clear()
        for x, y in self.grid.keys():
            button = Button(
                on_touch_down=self._which_touch_,
                on_press=lambda inst, x=x, y=y:
                    self.press(x, y) if self.current_button == "left" else self.flag(x, y),
                # text=str((x, y)),
                width=50,
                height=50,
                size_hint=(None, None),
            )
            self.buttons[(x, y)] = button
            self.add_widget(button)

    def _which_touch_(self, instance, touch):
        """This is a workaround because using on_touch_down directly causes all buttons to be activated"""
        self.current_button = touch.button

    def uncover(self, x, y):
            self.buttons[(x, y)].disabled = True
            self.grid.covered[x,y] = False

    def press(self, x, y):
        if self.buttons[(x, y)].text == self.FLAG_SYM:
            return
        elif len([c for c in self.buttons.values() if c.disabled]) == 0:
            self.grid.generate(((x, y),))
        if self.grid.is_bomb(x, y):
            self.uncover_all()
            self.buttons[(x, y)].background_color = (1, 0, 0, 1)
            return
        else:
            self.uncover(x, y)
            bombs = self.grid.adjacent_bombs(x, y)
            if len(bombs) == 0:
                for cell in self.grid.adjacent(x, y):
                    if self.grid.is_covered(*cell):
                        self.press(*cell)
            else:
                self.buttons[(x, y)].text = self.NUM_SYMS[len(bombs)]

        if len(self.grid.get_covered()) == self.grid.bomb_count:  # Win condition
            self.uncover_all()

    def flag(self, x, y):
        button = self.buttons[(x, y)]
        if button.text == self.FLAG_SYM:
            button.text = ''
        else:
            button.text = self.FLAG_SYM

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


class Game(App):
    def build(self):
        def _reload(inst):
            print("Reloading...")
            grid.reload()
            test_ai.reload()
        box_layout = BoxLayout(orientation="vertical")
        menu = BoxLayout(size_hint_y=None, height=35)
        grid = GridUI(30, 16, 11)
        test_ai = ai.simple.AI(grid)
        # Clock.schedule_interval(lambda dt: test_ai.solve(), 1.0)
        reload = Button(text="Reload", on_press=_reload)
        predict = Button(text="Predict", on_press=lambda dt: test_ai.solve())
        menu.add_widget(reload)
        menu.add_widget(predict)
        box_layout.add_widget(menu)
        box_layout.add_widget(grid)
        return box_layout
