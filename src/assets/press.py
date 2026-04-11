class Press:
    def __init__(self, press_id):
        self.press_id = press_id
        self.part = None

    def load_part(self, part):
        self.part = part

    def get_base_cycle_time(self):
        if not self.part:
            raise ValueError("No part loaded")
        return self.part.base_cycle_time