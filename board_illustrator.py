import drawSvg as draw
import numpy as np


class BoardDrawing(object):
    TILE_SIZE = 150
    STROKE = 2
    FONT_SIZE = 25
    TILES = {
        "brick": "img/production/Brick_med.png",
        "desert": "img/production/Desert_med.png",
        "ore": "img/production/Ore_med.png",
        "sheep": "img/production/Sheep_med.png",
        "wheat": "img/production/Wheat_med.png",
        "wood": "img/production/Wood_med.png",
        "ocean": "img/production/Ocean_med.png"
    }

    def __init__(self, number_matrix, tile_layout):
        self.file_name = "catan_board.svg"
        self.numbers = np.array(self._fill_sea(number_matrix))
        self.tiles = np.array(self._fill_sea(tile_layout, filler="Be"))
        if self.numbers.shape != self.tiles.shape:
            raise ValueError("Tile layout an number layout do not match")
        self.shape = self.numbers.shape
        self.drawing = draw.Drawing(self.shape[1] * self.TILE_SIZE + self.TILE_SIZE / 2 + 2 * self.STROKE,
                                    self.shape[0] * self.TILE_SIZE * 0.75 + self.TILE_SIZE * 0.25 + 2 * self.STROKE,
                                    overflow="hidden")
        self.drawing.viewBox = (self.TILE_SIZE / 4, self.TILE_SIZE / 2, self.drawing.width - self.TILE_SIZE,
                                self.drawing.height - self.TILE_SIZE / 2)
        self._init_tile_images()

    def generate_board_outline(self):
        for y, row in enumerate(self.tiles):
            for x, val in enumerate(row):
                if not val:
                    continue
                self.drawing.append(self._draw_hexagon(*self.get_hexagon_coords(x, y), val))

    def write_numbers(self):
        for y, row in enumerate(self.numbers):
            for x, val in enumerate(row):
                if not val:
                    continue
                number, weight, letter = val
                self.drawing.extend(self._draw_number(*self.get_hexagon_coords(x, y), letter))

    def save_output(self):
        with open(self.file_name, mode="w") as fp:
            self.drawing.asSvg(fp)

    def _draw_hexagon(self, x, y, val):
        return Polygon(points=[(int(x + self.TILE_SIZE / 2), int(y)),
                               (int(x + self.TILE_SIZE), int(y + self.TILE_SIZE / 4)),
                               (int(x + self.TILE_SIZE), int(y + 3 * self.TILE_SIZE / 4)),
                               (int(x + self.TILE_SIZE / 2), int(y + self.TILE_SIZE)),
                               (int(x), int(y + 3 * self.TILE_SIZE / 4)),
                               (int(x), int(y + self.TILE_SIZE / 4))
                               ], fill=f"url(#{val})", stroke="black")

    def _draw_number(self, x, y, val):
        text = draw.Text(str(val), self.FONT_SIZE, x + self.TILE_SIZE / 2, -(y + self.TILE_SIZE / 2), center=True)
        c_offset = self.TILE_SIZE / 2 + 3
        circle = draw.Circle(x + c_offset - 3, -(y + c_offset), r=self.FONT_SIZE * 0.75, fill="white", stroke="black")
        return [circle, text]

    def get_hexagon_coords(self, x, y):
        x_offset = (y % 2) * self.TILE_SIZE / 2
        return x * self.TILE_SIZE - x_offset, y * self.TILE_SIZE * 0.75

    def _init_tile_images(self):
        for tile_id, path in self.TILES.items():
            img = draw.Image(0, -1, 1, 1, "../" + path, mimeType=".png", embed=True, preserveAspectRatio="none")
            self.drawing.otherDefs.append(Pattern(children=[img], id=tile_id, height="100%", width="100%",
                                                  patternContentUnits="objectBoundingBox"))

    @staticmethod
    def _fill_sea(tile_layout, filler=None):
        row_len = 0
        for i, row in enumerate(tile_layout):
            row_len = len(row)
            if i % 2 == 0:
                tile_layout[i] = [filler] + row + [filler]
            else:
                tile_layout[i] = [filler] + row[1:] + [filler, filler]

        return [[filler] * (row_len + 2)] + tile_layout + [[filler] * (row_len + 2)]


class Polygon(draw.DrawingBasicElement):
    TAG_NAME = 'polygon'

    def __init__(self, points, **args):
        super().__init__(points=' '.join([f"{p[0]},{p[1]}" for p in points]), **args)


class Pattern(draw.DrawingParentElement):
    TAG_NAME = 'pattern'

    def __init__(self, children=(), **args):
        super().__init__(children=children, **args)
