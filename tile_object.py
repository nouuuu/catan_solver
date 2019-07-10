class CatanTile(object):

    def _init_(self, row, col, tile_type, **kwargs):
        self.row = row
        self.col = col
        self.tile_type = tile_type


class CatanLandTile(CatanTile):
    land_types = ["wood"], ['ore'], ['desert'], ['brick'], ['sheep'], ['wheat']

    def _init_(self, row, col, tile_type, letter_value, number_value):
        if tile_type not in self.land_types:
            raise ValueError(f"{tile_type} is not a land tile")
        super()._init_(row, col, tile_type)


class CatanSeaTile(CatanTile):
    land_types = ["sea", "harbour"]

    def _init_(self, row, col, tile_type, is_harbour, harbour_connections):
        if tile_type not in self.land_types:
            raise ValueError(f"{tile_type} is not a sea tile")
        super()._init_(row, col, tile_type)

# a_wood_tile = CatanLandTile(1, 2, "wood", "A", 4)
# a_harbour_tile = CatanSeaTile(1, 2, "harbour", True, [0, 4, 6])
