#!/usr/bin/env python3
import struct
import os
import colorama
import base64
import json
import json_fix

# Fine-tunables
NORMAL_LEVELS_OFFSET = 0x26E0A
NORMAL_LEVELS_SIZE = 0x500
NORMAL_LEVELS_NUM = 10
NORMAL_LEVELS_INIT_STATE_OFFSET = 0x257E8
SPECIAL_LEVEL_OFFSET = 0x25EA4
SPECIAL_LEVEL_SIZE = 70
BUGGY_LEVEL_OFFSET = 0x2932B
BUGGY_LEVEL_SIZE = 0x500
BUGGY_LEVEL_ID = 6
WARP_ZONE_LEVELS_DATA_OFFSET = 0x25862
WARP_ZONE_START_Y_OFFSET = 0x1710
WARP_ZONE_MOTION_FLAGS_OFFSET = 0x1716
WARP_ZONE_LEVEL_MAPPING_OFFSET = 0x2583A
MOTION_FLAG_MAPPINGS = { 0x24: 'stationary', 0x28: 'falling' }
PIXELS_PER_TILE = 16
FILENAME = 'DAVE.EXE'
TITLE_OFFSET = 0x2643F
TITLE_SIZE = 14
SUBTITLE_OFFSET = 0x26451
SUBTITLE_SIZE = 23

INIT_STATES_FMT = '<%dB%dH%dH' % (NORMAL_LEVELS_NUM, NORMAL_LEVELS_NUM, NORMAL_LEVELS_NUM)
WARP_ZONE_LEVEL_DATA_FMT = '<%dH%dH' % (NORMAL_LEVELS_NUM, NORMAL_LEVELS_NUM)
WARP_ZONE_MAPPINGS_FMT = '<%dH' % (NORMAL_LEVELS_NUM,)

# Initialize colors
colorama.init()
RESET_COLORS = colorama.Style.RESET_ALL
DIM = colorama.Style.DIM
BRIGHT = colorama.Style.BRIGHT
BLUE_FORE = colorama.Fore.BLUE
BLUE_BACK = colorama.Back.BLUE
RED_BACK = colorama.Back.RED
RED_FORE = colorama.Fore.RED 
CYAN_FORE = colorama.Fore.CYAN
CYAN_BACK = colorama.Back.CYAN
GREEN_FORE = colorama.Fore.GREEN
GREEN_BACK = colorama.Back.GREEN
YELLOW_FORE = colorama.Fore.YELLOW
YELLOW_BACK = colorama.Back.YELLOW
MAGENTA_FORE = colorama.Fore.MAGENTA
MAGENTA_BACK = colorama.Back.MAGENTA
WHITE_FORE = colorama.Fore.WHITE
WHITE_BACK = colorama.Back.WHITE
BLACK_FORE = colorama.Fore.BLACK
BLACK_BACK = colorama.Back.BLACK

# Logo
LOGO = base64.b64decode(b'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAbWzMxbV9fLC0tfi0tLl8bWzBtCiAgICAbWzM3bRtbMW3ilojilojilojilojilojilojilZcgIOKWiOKWiOKWiOKWiOKWiOKVlyDilojilojilZcgICDilojilojilZfilojilojilojilojilojilojilojilZcgICAg4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKVl+KWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVlyDilojilojilojilojilojilojilZcg4paI4paI4paI4paI4paI4paI4pWXG1swbSAgICAgICAgICAgICAbWzMxbSwtOzs7OyAgIGA7OztgXBtbMG0KICAgIBtbMzdtG1sxbeKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKVlOKVkOKVkOKVkOKVkOKVnSAgICDilojilojilZTilZDilZDilZDilZDilZ3ilojilojilZTilZDilZDilojilojilZfilojilojilZHilZrilZDilZDilojilojilZTilZDilZDilZ3ilojilojilZTilZDilZDilZDilojilojilZfilojilojilZTilZDilZDilojilojilZcbWzBtICAgICAgICAgICAbWzMxbS87Ozs7OyAgICAgIDs7OztgXBtbMG0KICAgIBtbMzdtG1sxbeKWiOKWiOKVkSAg4paI4paI4pWR4paI4paI4paI4paI4paI4paI4paI4pWR4paI4paI4pWRICAg4paI4paI4pWR4paI4paI4paI4paI4paI4pWXICAgICAg4paI4paI4paI4paI4paI4pWXICDilojilojilZEgIOKWiOKWiOKVkeKWiOKWiOKVkSAgIOKWiOKWiOKVkSAgIOKWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVnRtbMG0gICAgICAgICAbWzMxbS87Ozs7OzsgICAgIF9fXzs7XzsgXBtbMG0KICAgIBtbMzdtG1sxbeKWiOKWiOKVkSAg4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4paI4paI4pWR4pWa4paI4paI4pWXIOKWiOKWiOKVlOKVneKWiOKWiOKVlOKVkOKVkOKVnSAgICAgIOKWiOKWiOKVlOKVkOKVkOKVnSAg4paI4paI4pWRICDilojilojilZHilojilojilZEgICDilojilojilZEgICDilojilojilZEgICDilojilojilZHilojilojilZTilZDilZDilojilojilZcbWzBtICAgICAgICAbWzMxbS87Ozs7OzsgICAgICBcXyB8O3w7OyB8G1swbQogICAgG1szN20bWzFt4paI4paI4paI4paI4paI4paI4pWU4pWd4paI4paI4pWRICDilojilojilZEg4pWa4paI4paI4paI4paI4pWU4pWdIOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVlyAgICDilojilojilojilojilojilojilojilZfilojilojilojilojilojilojilZTilZ3ilojilojilZEgICDilojilojilZEgICDilZrilojilojilojilojilojilojilZTilZ3ilojilojilZEgIOKWiOKWiOKVkRtbMG0gICAgICAgG1szMW0bWzFtKDs7Ozs7OyAgICAgICBfX3x8X3w7Ozt8G1swbSAgIAogICAgG1szN20bWzFt4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWdIOKVmuKVkOKVnSAg4pWa4pWQ4pWdICDilZrilZDilZDilZDilZ0gIOKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVnSAgICDilZrilZDilZDilZDilZDilZDilZDilZ3ilZrilZDilZDilZDilZDilZDilZ0g4pWa4pWQ4pWdICAg4pWa4pWQ4pWdICAgIOKVmuKVkOKVkOKVkOKVkOKVkOKVnSDilZrilZDilZ0gIOKVmuKVkOKVnRtbMG0gICAgICAgIBtbMzFtG1sxbWBcXyw7OyAgICAgICAgICAgICA7XyxgXBtbMG0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIBtbMzFtG1sxbWBcX19fLC0tLS0tJ35+fn5+ICAgIGBcG1swbQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgG1szMW0bWzFtXCAgICAgICAgICAgICAgICAgICApG1swbQogICAgICAgICAgICAbWzMzbURhbmdlcm91cyBEYXZlICgxOTkwKSBlZGl0b3IgYnkgSm9uYXRoYW4gQmFyIE9yICgiSkJPIikbWzBtICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIBtbMzFtG1sxbWBcLl9fICAgICAgICAgICAgIC8nG1swbQogICAgICAgICAgICAgICAgICAgICAgICAbWzMzbWh0dHBzOi8veW8teW8teW8tamJvLmdpdGh1Yi5pbxtbMG0gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgG1szMW0bWzFtYH5+fn4tLS0tLS1+fhtbMG0KCg==').decode()

# Tile mappings
TILES = [('empty', ' '),
         ('crack1', f'{RED_FORE}{DIM}▚{RESET_COLORS}'),
         ('door', f'{RED_FORE}#{RESET_COLORS}'),
         ('girder_block', '▆'),
         ('jetpack', f'{GREEN_FORE}#{RESET_COLORS}'),
         ('bluewall', f'{BLUE_BACK} {RESET_COLORS}'),
         ('fire1', f'{RED_FORE}W{RESET_COLORS}'),
         ('fire2', f'{RED_FORE}W{RESET_COLORS}'),
         ('fire3', f'{RED_FORE}W{RESET_COLORS}'),
         ('fire4', f'{RED_FORE}W{RESET_COLORS}'),
         ('trophy1', f'{YELLOW_FORE}{BRIGHT}T{RESET_COLORS}'),
         ('trophy2', f'{YELLOW_FORE}{BRIGHT}T{RESET_COLORS}'),
         ('trophy3', f'{YELLOW_FORE}{BRIGHT}T{RESET_COLORS}'),
         ('trophy4', f'{YELLOW_FORE}{BRIGHT}T{RESET_COLORS}'),
         ('trophy5', f'{YELLOW_FORE}{BRIGHT}T{RESET_COLORS}'),
         ('pipe_horiz', f'{WHITE_FORE}{BRIGHT}{DIM}╣{RESET_COLORS}'),
         ('pipe_vert', f'{WHITE_FORE}{BRIGHT}{DIM}╩{RESET_COLORS}'),
         ('redwall', f'{RED_BACK} {RESET_COLORS}'),
         ('crack2', f'{RED_FORE}{DIM}▚{RESET_COLORS}'),
         ('bluetile', f'{BLUE_BACK}{CYAN_FORE}▚{RESET_COLORS}'),
         ('gun', '╤'),
         ('diag1', f'{RED_FORE}{DIM}▙{RESET_COLORS}'),
         ('diag2', f'{RED_FORE}{DIM}▟{RESET_COLORS}'),
         ('diag3', f'{RED_FORE}{DIM}▜{RESET_COLORS}'),
         ('diag4', f'{RED_FORE}{DIM}▛{RESET_COLORS}'),
         ('tent1', f'{MAGENTA_FORE}|{RESET_COLORS}'),
         ('tent2', f'{MAGENTA_FORE}|{RESET_COLORS}'),
         ('tent3', f'{MAGENTA_FORE}|{RESET_COLORS}'),
         ('tent4', f'{MAGENTA_FORE}|{RESET_COLORS}'),
         ('girder_vert', f'{MAGENTA_FORE}{DIM}▐{RESET_COLORS}'),
         ('girder_horiz1', f'{MAGENTA_FORE}{DIM}▄{RESET_COLORS}'),
         ('girder_horiz2', f'{MAGENTA_FORE}{DIM}▄{RESET_COLORS}'),
         ('low_grass', f'{GREEN_FORE}_{RESET_COLORS}'),
         ('trunk', f'{RED_FORE}|{RESET_COLORS}'),
         ('branch1', f'{GREEN_FORE}O{RESET_COLORS}'),
         ('branch2', f'{GREEN_FORE}O{RESET_COLORS}'),
         ('water1', f'{CYAN_BACK}{BLUE_FORE}▓{RESET_COLORS}'),
         ('water2', f'{CYAN_BACK}{BLUE_FORE}▓{RESET_COLORS}'),
         ('water3', f'{CYAN_BACK}{BLUE_FORE}▓{RESET_COLORS}'),
         ('water4', f'{CYAN_BACK}{BLUE_FORE}▓{RESET_COLORS}'),
         ('water5', f'{CYAN_BACK}{BLUE_FORE}▓{RESET_COLORS}'),
         ('stars', f'{WHITE_FORE}{BRIGHT}.{RESET_COLORS}'),
         ('moon', f'{WHITE_FORE}{BRIGHT}<{RESET_COLORS}'),
         ('branch3', f'{GREEN_FORE}O{RESET_COLORS}'),
         ('branch4', f'{GREEN_FORE}O{RESET_COLORS}'),
         ('branch5', f'{GREEN_FORE}O{RESET_COLORS}'),
         ('branch6', f'{GREEN_FORE}O{RESET_COLORS}'),
         ('diamond_blue', f'{CYAN_FORE}{BRIGHT}*{RESET_COLORS}'),
         ('purple_dot', f'{MAGENTA_FORE}*{RESET_COLORS}'),
         ('diamond_red', f'{RED_FORE}{BRIGHT}*{RESET_COLORS}'),
         ('crown', f'{YELLOW_FORE}{BRIGHT}M{RESET_COLORS}'),
         ('ring', f'{YELLOW_FORE}{BRIGHT}O{RESET_COLORS}'),
         ('septer', f'{GREEN_FORE}/{RESET_COLORS}'), 
         ('dave1', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('dave2', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('dave3', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('dave4', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('dave5', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('dave6', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('dave7', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('shadow1', ' '),
         ('shadow2', ' '),
         ('shadow3', ' '),
         ('shadow4', ' '),
         ('shadow5', ' '),
         ('shadow6', ' '),
         ('shadow7', ' '),
         ('jump_right', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('jump_left', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('shadow_right', ' '),
         ('shadow_left', ' '),
         ('climb1', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('climb2', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('climb3', f'{RED_FORE}{DIM}D{RESET_COLORS}'),
         ('shadow_climb1', ' '),
         ('shadow_climb2', ' '),
         ('shadow_climb3', ' '),
         ('jetpack_right1', f'{RED_FORE}{DIM}{GREEN_BACK}D{RESET_COLORS}'),
         ('jetpack_right2', f'{RED_FORE}{DIM}{GREEN_BACK}D{RESET_COLORS}'),
         ('jetpack_right3', f'{RED_FORE}{DIM}{GREEN_BACK}D{RESET_COLORS}'),
         ('jetpack_left1', f'{RED_FORE}{DIM}{GREEN_BACK}D{RESET_COLORS}'),
         ('jetpack_left2', f'{RED_FORE}{DIM}{GREEN_BACK}D{RESET_COLORS}'),
         ('jetpack_left3', f'{RED_FORE}{DIM}{GREEN_BACK}D{RESET_COLORS}'),
         ('jetpack_shadow_right1', ' '),
         ('jetpack_shadow_right2', ' '),
         ('jetpack_shadow_right3', ' '),
         ('jetpack_shadow_left1', ' '),
         ('jetpack_shadow_left2', ' '),
         ('jetpack_shadow_left3', ' '),
         ('spider1', 'S'),
         ('spider2', 'S'),
         ('spider3', 'S'),
         ('spider4', 'S'),
         ('shuriken1', '@'),
         ('shuriken2', '@'),
         ('shuriken3', '@'),
         ('shuriken4', '@'),
         ('lili1', 'L'),
         ('lili2', 'L'),
         ('lili3', 'L'),
         ('lili4', 'L'),
         ('stick1', 'F'),
         ('stick2', 'F'),
         ('stick3', 'F'),
         ('stick4', 'F'),
         ('ufo1', 'v'),
         ('ufo2', 'v'),
         ('ufo3', 'v'),
         ('ufo4' ,'v'),
         ('burger1', 'b'),
         ('burget2', 'b'),
         ('burget3', 'b'),
         ('burget4', 'b'),
         ('green_ball1', f'{GREEN_FORE}{DIM}O{RESET_COLORS}'),
         ('green_ball2', f'{GREEN_FORE}{DIM}O{RESET_COLORS}'),
         ('green_ball3', f'{GREEN_FORE}{DIM}O{RESET_COLORS}'),
         ('green_ball4', f'{GREEN_FORE}{DIM}O{RESET_COLORS}'),
         ('saucer1', 's'),
         ('saucer2', 's'),
         ('saucer3', 's'),
         ('saucer4', 's'),
         ('shot_right1', ']'),
         ('shot_right2', ']'),
         ('shot_right3', ']'),
         ('shot_left1', '['),
         ('shot_left2', '['),
         ('shot_left3', '['),
         ('bullet_right', '>'),
         ('bullet_left', '<'),
         ('explode1', '!'),
         ('explode2', '!'),
         ('explode3', '!'),
         ('explode4', '!'),
         ('label_jetpack', ' '),
         ('label_gun', ' '),
         ('label_lives', ' '),
         ('label_level', ' '),
         ('label_score', ' '),
         ('label_go', ' '),
         ('label_warp', ' '),
         ('label_zone', ' '),
         ('frame', ' '),
         ('red_right', ' '),
         ('lives_face', 'L'),
         ('intro1', ' '),
         ('intro2', ' '),
         ('intro3', ' '),
         ('intro4', ' '),
         ('num0', '0'),
         ('num1', '1'),
         ('num2', '2'),
         ('num3', '3'),
         ('num4', '4'),
         ('num5', '5'),
         ('num6', '6'),
         ('num7', '7'),
         ('num8', '8'),
         ('num9', '9') ]

def clear_screen():
    """
        Clears the screen.
    """

    # Act based on OS
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    # Print logo
    print(f'{WHITE_FORE}{BRIGHT}{LOGO}{RESET_COLORS}')

def pixel_to_tile_coord_x(p):
    """
        Translates pixel numbers to a tile X cooredinate.
    """

    # Return the result
    return p // PIXELS_PER_TILE

def pixel_to_tile_coord_y(p):
    """
        Translates pixel numbers to a tile X cooredinate.
    """

    # Return the result
    return p // PIXELS_PER_TILE - 1

def tile_coord_x_to_pixel(p):
    """
        Translates pixel numbers to a tile X cooredinate.
    """

    # Return the result
    return p * PIXELS_PER_TILE

def tile_coord_y_to_pixel(p):
    """
        Translates pixel numbers to a tile Y cooredinate.
    """

    # Return the result
    return (p + 1) * PIXELS_PER_TILE 

class WarpZoneInfo(object):
    """
        Represents Warp Zone information.
    """

    @staticmethod
    def parse():
        """
            Parses all the warp zones from the binary bytes.
            Returns None for levels that do not have warp-zones.
        """
        global bin_bytes
        # Extract per-level warp zone data 
        warp_zone_level_data = struct.unpack(WARP_ZONE_LEVEL_DATA_FMT, bin_bytes[WARP_ZONE_LEVELS_DATA_OFFSET:WARP_ZONE_LEVELS_DATA_OFFSET + struct.calcsize(WARP_ZONE_LEVEL_DATA_FMT)])

        # Extract the global data for warp zones
        warp_zone_start_y = pixel_to_tile_coord_y(struct.unpack('<H', bin_bytes[WARP_ZONE_START_Y_OFFSET:WARP_ZONE_START_Y_OFFSET + struct.calcsize('<H')])[0])
        warp_zone_init_motion = MOTION_FLAG_MAPPINGS[struct.unpack('<H', bin_bytes[WARP_ZONE_MOTION_FLAGS_OFFSET:WARP_ZONE_MOTION_FLAGS_OFFSET + struct.calcsize('<H')])[0]]

        # Extract warp-level mapping
        warp_mappings = struct.unpack(WARP_ZONE_MAPPINGS_FMT, bin_bytes[WARP_ZONE_LEVEL_MAPPING_OFFSET:WARP_ZONE_LEVEL_MAPPING_OFFSET + struct.calcsize(WARP_ZONE_MAPPINGS_FMT)])
        
        # Return all parsed warp zones
        zones = []
        for i in range(NORMAL_LEVELS_NUM):
            horiz_scroll = warp_zone_level_data[NORMAL_LEVELS_NUM + i]
            if horiz_scroll == 0:
                zones.append(None)
            else:
                zones.append(WarpZoneInfo(pixel_to_tile_coord_x(horiz_scroll), warp_zone_level_data[i], warp_zone_start_y, warp_zone_init_motion, warp_mappings[i]))
        return zones

    def __init__(self, zoneStartx, daveStartx, starty, init_motion, warp_level):
        """
            Initializes.
        """

        # Saves data
        self.zoneStartx = zoneStartx
        self.daveStartx = daveStartx
        self.starty = starty
        self.init_motion = init_motion
        self.warp_level = warp_level

    def __json__(self):
        obj = {
            "zoneStartx": self.zoneStartx,
            "daveStartx": self.daveStartx,
            "warp_level": self.warp_level,
        }
        
        return obj

    def __str__(self):
        """
            Returns a nice text-representation of the warp-zone information.
        """

        # Build the warp zone information
        return 'Warp zone mapped to level %d starts at (%d, %d) while %s.' % (self.warp_level, self.zoneStartx + self.daveStartx, self.starty, self.init_motion)

class Level(object):
    """
        Represents a Level in DAVE.
    """

    @staticmethod
    def parse(bin_bytes):
        """
            Parses all the levels from the binary bytes.
        """

        # Start with the special level
        levels = [ Level(0).withBytes(bin_bytes[SPECIAL_LEVEL_OFFSET:SPECIAL_LEVEL_OFFSET + SPECIAL_LEVEL_SIZE], 'Intro screen') ]

        # Parse initial state for all normal levels
        init_states = struct.unpack(INIT_STATES_FMT, bin_bytes[NORMAL_LEVELS_INIT_STATE_OFFSET:NORMAL_LEVELS_INIT_STATE_OFFSET + struct.calcsize(INIT_STATES_FMT)])

        # Parse warp zones for normal levels
        warp_zones = WarpZoneInfo.parse()

        # Parse normal levels
        for i in range(NORMAL_LEVELS_NUM):
            data = bin_bytes[NORMAL_LEVELS_OFFSET + (NORMAL_LEVELS_SIZE*i):NORMAL_LEVELS_OFFSET + NORMAL_LEVELS_SIZE*(i+1)]
            init_motion, startx, starty = init_states[i], pixel_to_tile_coord_x(init_states[NORMAL_LEVELS_NUM + i]), pixel_to_tile_coord_y(init_states[2*NORMAL_LEVELS_NUM + i])
            levels.append(Level(i + 1).withBytes(data, 'Level %d' % (i+1,), startx, starty, MOTION_FLAG_MAPPINGS[init_motion], warp_zones[i]))

        # Parse the buggy warp zone level
        levels.append(Level(11).withBytes(bin_bytes[BUGGY_LEVEL_OFFSET:BUGGY_LEVEL_OFFSET + BUGGY_LEVEL_SIZE], 'Buggy warp level'))

        # Return all the levels
        return levels

    @staticmethod
    def get_tile(index):
        """
            Return the tile representation.
        """

        # Default representatiob of unknown tiles
        if len(TILES) <= index:
            return f'{WHITE_BACK}{BRIGHT}?{RESET_COLORS}'
        return TILES[index][1]

    def __init__(self, levelNum):
        self.num = levelNum
        self.width = 100
        self.height = 10
        if levelNum == 0:
            self.tiles_offset = SPECIAL_LEVEL_OFFSET
            self.width = 7
            self.height = 10
        elif levelNum < 11:
            self.tiles_offset = NORMAL_LEVELS_OFFSET + (NORMAL_LEVELS_SIZE*(levelNum - 1)) + 256
        else:
            self.tiles_offset = BUGGY_LEVEL_OFFSET + 256
            
        self.title = ""
        
    def withBytes(self, level_bytes, level_title, startx=0, starty=0, init_motion=None, warp_zone=None):
        """
            Initializes.
        """

        self.startx = startx
        self.starty = starty

        # Handle level data
        if len(level_bytes) == 1280:
            self.path_data = level_bytes[:256]
            self.tiles = [ tile for tile in level_bytes[256:-24] ]
            self.width = 100
            self.height = 10
        elif len(level_bytes) == 70:
            self.path_data = b''
            self.tiles = [ tile for tile in level_bytes[:] ]
            self.width = 10
            self.height = 7
        else:
            raise Exception('Invalid level length %d' % (len(level_bytes),))

        # Save the title
        if init_motion is not None:
            self.title = '%s (start at (%d, %d) %s)' % (level_title, startx, starty, init_motion)
        else:
            self.title = level_title

        # Save warp zone (might be None)
        self.warp_zone = warp_zone
        
        return self
      
    def withObj(self, obj):
        self.tiles = list(obj.get('tiles'))
        self.path_data = bytes(obj.get('path_data'))
        self.startx = obj.get('startx')
        self.starty = obj.get('starty')
        
        self.startxPix = tile_coord_x_to_pixel(self.startx)
        self.startyPix = tile_coord_y_to_pixel(self.starty)

        w = obj.get('warp_zone')
        
        if w is not None :
            self.warp_zone = WarpZoneInfo(w.get('zoneStartx'), w.get('daveStartx'), 0, "falling", w.get('warp_level'))
        else:
            self.warp_zone = None
        return self
    
    def __json__(self):
        obj = { 
            "path_data": list(map(int, [x for x in self.path_data])),
            "tiles": self.tiles,
            "warp_zone": self.warp_zone,
            "startx": self.startx,
            "starty": self.starty,
            "tiles_offset": self.tiles_offset
        }
        
        return obj
        
        
    def __str__(self):
        """
            Returns a nice string-representation of the level.
        """
        # Returns the text representation
        self_repr = self.title + ':\n\n '
        for i in range(self.width):
            if i%10 == 0:
                self_repr += str(int(i/10))
            else:
                self_repr += ' '
        self_repr += '\n '
        for i in range(self.width):    
            self_repr += str(i%10) 

        self_repr += '\n'
        
        for i in range(0, len(self.tiles), self.width):
            self_repr += str(int(i/self.width))
            for tile in self.tiles[i:i+self.width]:
                self_repr += Level.get_tile(tile)
            self_repr += '\n'
        
        if self.warp_zone is not None:
            self_repr += '\n\n%s' % (self.warp_zone,)
        return self_repr

def choose_level(num_levels):
    """
        Chooses a level number.
    """

    # Present choice
    num_level = input('Choose level number (0-%d): ' % (num_levels - 1,))
    if num_level.isdigit() and int(num_level) >= 0 and int(num_level) < num_levels:
        return int(num_level)
    else:
        raise Exception('Invalid level number: %s.' % (num_level,))

def get_coord(coord_type, max_num):
    """
        Gets a coordinate.
    """

    # Get input
    coord = input('Enter %s coordinate (0-%d): ' % (coord_type, max_num - 1))
    if coord.isdigit() and int(coord) >= 0 and int(coord) < max_num:
        return int(coord)
    else:
        raise Exception('Invalid %s coordinate: %s.' % (coord_type, coord))

bin_bytes = None
def main():
    """
        Main functionality.
    """

    global bin_bytes
    # Handle critical errors
    try:

        # Parse DAVE.EXE
        with open(FILENAME, 'rb') as f:
            bin_bytes = f.read()

        # Parse levels
        levels = Level.parse(bin_bytes)
        if len(levels) == 0:
            raise Exception('Error parsing levels.')

        # Extract title and subtitle
        titles = [ bin_bytes[TITLE_OFFSET:TITLE_OFFSET + TITLE_SIZE].decode(), bin_bytes[SUBTITLE_OFFSET:SUBTITLE_OFFSET + SUBTITLE_SIZE].decode() ]

    except Exception as ex:
        print('Fatal error: %s' % (ex,))
        return

    # Handle menu
    clear_screen()
    saved = True
    while True:

        # Handle all exceptions
        try:

            # Present header
            print(f'Loaded {BLUE_FORE}{BRIGHT}{len(levels)}{RESET_COLORS} levels.')
            print(f'Current intro title: {BLUE_FORE}{BRIGHT}"{titles[0]}"{RESET_COLORS}.')
            print(f'Current intro subtitle: {BLUE_FORE}{BRIGHT}"{titles[1]}"{RESET_COLORS}.')
            if not saved:
                print(f'You have {RED_FORE}UNSAVED{RESET_COLORS} edits.\n')
            print(f'\n{YELLOW_FORE}== MENU =={RESET_COLORS}\n\t[{YELLOW_FORE}V{RESET_COLORS}]iew a level.\n\t[{YELLOW_FORE}E{RESET_COLORS}]dit a level.\n\tEdit intro [{YELLOW_FORE}T{RESET_COLORS}]itle.\n\tEdit intro su[{YELLOW_FORE}B{RESET_COLORS}]title.\n\t[{YELLOW_FORE}S{RESET_COLORS}]ave pending changes.\n\t[{YELLOW_FORE}Q{RESET_COLORS}]uit without saving.\n\n{YELLOW_FORE}== JSON =={RESET_COLORS}\n\t[{YELLOW_FORE}J{RESET_COLORS}]son dump into dave.json.\n\t[{YELLOW_FORE}L{RESET_COLORS}]oad from dave.json.')
            choice = input('> ').upper()
           
            # Handle title or subtitle changes
            if choice == 'T' or choice == 'B':
                title_index = 0 if choice == 'T' else 1
                print('Current intro %s: "%s".' % ('title' if choice == 'T' else 'subtitle', titles[title_index]))
                new_text = input('New %s (AT MOST %d characters): ' % ('title' if choice == 'T' else 'subtitle', len(titles[title_index])))
                if len(new_text) > len(titles[title_index]):
                    raise Exception('Length of new %s is too big (max=%d).' % ('title' if choice == 'T' else 'subtitle', len(titles[title_index])))
                spaces =  len(titles[title_index]) - len(new_text)
                for i in range(spaces // 2):
                    new_text = ' ' + new_text + ' '
                if spaces % 2 == 1:
                    new_text += ' '
                titles[title_index] = new_text
                saved = False
                clear_screen()
                print('Changed %s successfully.' % ('title' if choice == 'T' else 'subtitle',))
                continue

            # Handle edit\view
            if choice == 'V' or choice == 'E':
                level_num = choose_level(len(levels))
                clear_screen()
                print(levels[int(level_num)])
                print('\n\n')
                if choice == 'E':
                    x_coord = get_coord('X', levels[level_num].width)
                    y_coord = get_coord('Y', levels[level_num].height)
                    tile_index = levels[level_num].tiles[y_coord * levels[level_num].height+ x_coord]
                    if tile_index >= len(TILES):
                        raise Exception('Cannot edit unknown tile for level %d at position (%d, %d).' % (level_num, x_coord, y_coord))
                    print('Current tile is %s.' % (TILES[tile_index][0],))
                    print('Available tile types: %s' % (', '.join( [tile[0] for tile in TILES ])))
                    new_tile = input('New tile type: ')
                    matched_tiles = [ tile_index for tile_index in range(len(TILES)) if TILES[tile_index][0] == new_tile ]
                    if len(matched_tiles) != 1:
                        raise Exception('Invalid tile type: %s.' % (new_tile,))
                    if TILES[matched_tiles[0]] != TILES[tile_index][0]:
                        levels[level_num].tiles[y_coord * levels[level_num].width+ x_coord] = matched_tiles[0]
                        saved = False
                        clear_screen()
                        print('Level %d patched successfully.' % (level_num,))
                continue
            
            # Handle saving
            if choice == 'S':
                if saved:
                    print('Nothing to save.')
                    continue
                choice = input(f'This will completely override file %s! Choose \'{YELLOW_FORE}Y{RESET_COLORS}\' to do it or any key to cancel: ' % (FILENAME,)).upper()
                if choice != 'Y':
                    continue
                new_bytes = bin_bytes[:]

                warp_zone_level_data_dict = {}
                warp_mappings = []
                init_states_dict = {}
                touched_extra = False
                i = -2
                for level in levels:
                    i += 1
                    new_bytes = new_bytes[:level.tiles_offset] + bytes(level.tiles) + new_bytes[level.tiles_offset + len(level.tiles):]
                    
                    if i >= 0 and i < 10 and hasattr(level,'startxPix'):
                        touched_extra = True
                        init_states_dict[i] = 0x24
                        init_states_dict[NORMAL_LEVELS_NUM + i] = level.startxPix
                        init_states_dict[2*NORMAL_LEVELS_NUM + i] = level.startyPix
                        if level.warp_zone is not None:
                            warp_zone = level.warp_zone
                            warp_mappings.append(warp_zone.warp_level)
                            warp_zone_level_data_dict[NORMAL_LEVELS_NUM + i] = tile_coord_x_to_pixel(warp_zone.zoneStartx)
                            warp_zone_level_data_dict[i] = warp_zone.daveStartx
                        else:
                            warp_mappings.append(0)
                            warp_zone_level_data_dict[NORMAL_LEVELS_NUM + i] = 0
                            warp_zone_level_data_dict[i] = 0
                    
                new_bytes = new_bytes[:TITLE_OFFSET] + titles[0].encode() + new_bytes[TITLE_OFFSET + TITLE_SIZE:]
                new_bytes = new_bytes[:SUBTITLE_OFFSET] + titles[1].encode() + new_bytes[SUBTITLE_OFFSET + SUBTITLE_SIZE:]
                
                if touched_extra:

                    warp_zone_level_data = tuple([warp_zone_level_data_dict[field] for field in dict(sorted(warp_zone_level_data_dict.items(), key=lambda x: x[0]))])
                    x = struct.pack(WARP_ZONE_LEVEL_DATA_FMT, *warp_zone_level_data)
                    new_bytes = new_bytes[:WARP_ZONE_LEVELS_DATA_OFFSET] + x + new_bytes[WARP_ZONE_LEVELS_DATA_OFFSET + struct.calcsize(WARP_ZONE_LEVEL_DATA_FMT):]
            
                    x = struct.pack(WARP_ZONE_MAPPINGS_FMT, *warp_mappings)
                    new_bytes = new_bytes[:WARP_ZONE_LEVEL_MAPPING_OFFSET] + x + new_bytes[WARP_ZONE_LEVEL_MAPPING_OFFSET + struct.calcsize(WARP_ZONE_MAPPINGS_FMT):]
                
                    init_states = tuple([init_states_dict[field] for field in dict(sorted(init_states_dict.items(), key=lambda x: x[0]))])
                    x = struct.pack(INIT_STATES_FMT, *init_states)
                    new_bytes = new_bytes[:NORMAL_LEVELS_INIT_STATE_OFFSET] + x + new_bytes[NORMAL_LEVELS_INIT_STATE_OFFSET + struct.calcsize(INIT_STATES_FMT):]
                
                with open(FILENAME, 'wb') as f:
                    f.write(new_bytes)
                clear_screen()
                print('Written %d bytes to file %s successfully.' % (len(bin_bytes), FILENAME))
                saved = True
                continue

            # Handle quitting
            if choice == 'Q':
                if not saved:
                    choice = input(f'All your changed will be lost! Choose \'{YELLOW_FORE}Y{RESET_COLORS}\' to quit or any key to cancel: ').upper()
                    if choice != 'Y':
                        continue
                print('Quitting.\n')
                break
            
            if choice == 'J':
                jd = json.dumps(
                    levels,
                    sort_keys=True,
                    indent=4
                ) 
                with open("dave.json", 'w') as f:
                    f.write(jd)
                print(f"Write Successful to dave.json. Now, open this file in browser, edit, download and overwrite in folder, load with '{YELLOW_FORE}L{RESET_COLORS}' option and save dave.exe.\n\n")
                continue

            if choice == 'L':
                with open('dave.json') as json_data:
                    d = json.load(json_data)

                levels = []
                levelNum = 0
                for level in d:
                    levels.append(Level(levelNum).withObj(level))
                    levelNum = levelNum + 1
                print(f"Load Successful from dave.json! You may save with '{YELLOW_FORE}S{RESET_COLORS}' option.\n\n")
                saved = False
                continue

            # Default handling
            raise Exception('Invalid option: %s\n' % (choice,))

        # Handle exceptions
        except Exception as ex:
            clear_screen()
            print(ex)



def ins_tup(tuple, i, value): 

    tuple = tuple[:i] + (value,) + tuple[i+1:]
    return tuple

if __name__ == '__main__':
    main()