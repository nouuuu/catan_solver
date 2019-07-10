from itertools import chain

import drawSvg as draw
import numpy as np
from numpy.random import randint


class BoardDrawing(object):
    #if printed on A1 350 is the appropriate tile size
    TILE_SIZE = 350
    HALF_TILE = TILE_SIZE / 2
    QUARTER_TILE = TILE_SIZE / 4
    STROKE = TILE_SIZE / 30
    FONT_SIZE = TILE_SIZE / 6
    HEX_COEFF = np.math.sqrt(3) / 2
    TILES = {
        "brick": "img/production/Brick_med.png",
        "desert": "img/production/Desert_med.png",
        "ore": "img/production/Ore_med.png",
        "sheep": "img/production/Sheep_med.png",
        "wheat": "img/production/Wheat_med.png",
        "wood": "img/production/Wood_med.png",
        "ocean": "img/production/Ocean_med.png",
        "question_mark" : "img/production/question_mark.png"
    }

    NEIGHBOURS = {0: [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1)],
                  1: [(-1, 0), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1), ]}

    def __init__(self, number_matrix, tile_layout):
        self.file_name = "catan_board.svg"
        self.numbers = np.array(self._fill_sea(number_matrix))
        self.tiles = np.array(self._fill_sea(tile_layout, filler="ocean"), dtype='U8')
        if self.numbers.shape != self.tiles.shape:
            raise ValueError("Tile layout an number layout do not match")
        self.shape = self.numbers.shape
        self.drawing = draw.Drawing((self.shape[1] - 2.5) * self.TILE_SIZE,
                                    (self.shape[0] - 1.5) * self.TILE_SIZE * self.HEX_COEFF,
                                    overflow="hidden")
        self.drawing.viewBox = (-self.QUARTER_TILE, -self.QUARTER_TILE, self.drawing.width,
                                self.drawing.height)
        self._init_tile_images()

    def generate_board_outline(self):
        for y, row in enumerate(self.tiles):
            for x, val in enumerate(row):
                if not val:
                    continue
                self.drawing.append(self._draw_hexagon(*self._get_hexagon_coords(x, y), val))

    def write_numbers(self):
        for y, row in enumerate(self.numbers):
            for x, val in enumerate(row):
                # self.drawing.extend(self._draw_coordinates(*self._get_hexagon_coords(x, y), x, y))
                if not val:
                    continue
                number, weight, letter = val
                self.drawing.extend(self._draw_number(*self._get_hexagon_coords(x, y), number))

    def save_output(self):
        with open(self.file_name, mode="w") as fp:
            self.drawing.asSvg(fp)

    def _draw_hexagon(self, x, y, val, rotation=None):
        def pointy_hex_corner(x, y, i):
            angle_rad = np.math.pi * (i / 3 - 1 / 6)
            return x + self.HALF_TILE * np.math.cos(angle_rad), y + self.HALF_TILE * np.math.sin(angle_rad)

        if rotation is None:
            rotation = randint(0, 6) * 60
        rotation = int(np.math.ceil(rotation / 60.0) * 60)
        return Polygon(points=[pointy_hex_corner(x, y, i) for i in range(0, 6)], fill=f"url(#{val})", stroke="black",
                       transform=f"rotate({rotation},{x},{y})", **{"stroke-width": self.STROKE})

    def _draw_number(self, x, y, val):
        text = draw.Text(str(val), self.FONT_SIZE, x-1, -(y-2), center=True)
        circle = draw.Circle(x, -(y + 4), r=self.FONT_SIZE * 0.75, fill="beige", stroke="black")
        return [circle, text]

    def _get_hexagon_coords(self, x, y):
        # r-odd grid layout x = col, y = row
        x_offset = (y % 2) * self.HALF_TILE
        return int((x * self.TILE_SIZE - x_offset) * self.HEX_COEFF), int(y * self.TILE_SIZE * 0.75)

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

    def draw_harbours(self, harbour_list):
        for col, row, adj_tiles, harbour_type in harbour_list:
            c_x, c_y = self._get_hexagon_coords(col, row)
            text = "3 : 1"
            val = "question_mark"
            if harbour_type[0] == "2":
                text = "2 : 1"
                val = harbour_type.split("_")[3]
            t = draw.Text(text, 42, c_x, -(c_y + 50), center=True, stroke="beige")
            c = draw.Circle(c_x, -c_y, r=42, fill=f"url(#{val})", stroke="black")
            n = set(chain.from_iterable([(a, b) for _, _, type, a, b in adj_tiles if not type == 'harbour']))
            # 0 = 90° theta, 1= 30*,  2 = -30°, 3 = - 90°
            for corner in n:
                theta = 90 - corner * 60
                e_x = int(self.HALF_TILE * np.math.cos(np.math.radians(theta)) + c_x)
                e_y = int(self.HALF_TILE * np.math.sin(np.math.radians(theta)) + c_y)
                line = draw.Line(c_x, -c_y, e_x, -e_y,
                                 **{"stroke": "black", "stroke-dasharray": "10 10", "stroke-width": "5px"})
                self.drawing.extend([line])
            self.drawing.extend([c, t])

    def _draw_coordinates(self, bx, by, x, y):
        cx = bx - self.QUARTER_TILE
        cy = -(by - self.QUARTER_TILE)
        text = draw.Text(f"{x}, {y}", 18, cx, cy, center=True)
        circle = draw.Circle(cx, cy, r=18, fill="white", stroke="black")
        return [circle, text]


class Polygon(draw.DrawingBasicElement):
    TAG_NAME = 'polygon'

    def __init__(self, points, **args):
        super().__init__(points=' '.join([f"{p[0]},{p[1]}" for p in points]), **args)


class Pattern(draw.DrawingParentElement):
    TAG_NAME = 'pattern'

    def __init__(self, children=(), **args):
        super().__init__(children=children, **args)
