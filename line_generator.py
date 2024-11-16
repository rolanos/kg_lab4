import random

class LineGenerator:
    def __init__(self, num_lines=20):
        self.num_lines = num_lines

    def generate_lines(self):
        lines = []
        for _ in range(self.num_lines):
            x1, y1 = random.randint(50, 750), random.randint(50, 550)
            x2, y2 = random.randint(50, 750), random.randint(50, 550)
            lines.append(((x1, y1), (x2, y2)))
        return lines
