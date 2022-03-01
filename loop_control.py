class LoopControl():

    def __init__(self) -> None:
        self.key_pressed = False
        self.paused = False
        self.run = True

    def pause(self):
        self.paused = not self.paused
        self.run = not self.run