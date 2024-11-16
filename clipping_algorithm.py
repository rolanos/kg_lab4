class ClippingAlgorithm:
    def __init__(self, clip_window):
        self.x_min, self.y_min, self.x_max, self.y_max = clip_window

    def clip_lines(self, lines):
        clipped_lines = []
        for line in lines:
            clipped_line = self.cohen_sutherland_clip(line)
            if clipped_line:
                clipped_lines.append(clipped_line)
        return clipped_lines

    def cohen_sutherland_clip(self, line):
        x1, y1 = line[0]
        x2, y2 = line[1]
        code1 = self.compute_out_code(x1, y1)
        code2 = self.compute_out_code(x2, y2)

        while True:
            if code1 == 0 and code2 == 0:  # Trivially accepted
                return (x1, y1), (x2, y2)
            elif (code1 & code2) != 0:  # Trivially rejected
                return None
            else:
                x, y = 0, 0
                outcode_out = code1 if code1 != 0 else code2
                if outcode_out & 8:
                    x = x1 + (x2 - x1) * (self.y_max - y1) / (y2 - y1)
                    y = self.y_max
                elif outcode_out & 4:
                    x = x1 + (x2 - x1) * (self.y_min - y1) / (y2 - y1)
                    y = self.y_min
                elif outcode_out & 2:
                    y = y1 + (y2 - y1) * (self.x_max - x1) / (x2 - x1)
                    x = self.x_max
                elif outcode_out & 1:
                    y = y1 + (y2 - y1) * (self.x_min - x1) / (x2 - x1)
                    x = self.x_min
                if outcode_out == code1:
                    x1, y1 = x, y
                    code1 = self.compute_out_code(x1, y1)
                else:
                    x2, y2 = x, y
                    code2 = self.compute_out_code(x2, y2)

    def compute_out_code(self, x, y):
        code = 0
        if x < self.x_min:
            code |= 1
        elif x > self.x_max:
            code |= 2
        if y < self.y_min:
            code |= 4
        elif y > self.y_max:
            code |= 8
        return code
