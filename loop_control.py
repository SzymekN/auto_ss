class LoopControl():

    def __init__(self) -> None:
        self.key_pressed = False
        self.paused = False
        self.run = True
        self.delay = 1

    def pause(self):
        self.paused = not self.paused
        self.run = not self.run

    def change_delay(self, value):
        if value:
            self.delay += 1
        else:
            if self.delay > 0: 
                self.delay -= 1