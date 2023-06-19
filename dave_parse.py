#!/usr/bin/env python3
import struct
import binascii
import os

# Fine-tunables
NORMAL_LEVELS_OFFSET = 0x26E0A
NORMAL_LEVELS_SIZE = 0x500
NORMAL_LEVELS_NUM = 10
NORMAL_LEVELS_INIT_STATE_OFFSET = 0x257E8
SPECIAL_LEVEL_OFFSET = 0x25EA4
SPECIAL_LEVEL_SIZE = 70
BUGGY_LEVEL_OFFSET = 0x2932B
BUGGY_LEVEL_SIZE = 0x500
WARP_ZONE_LEVELS_DATA_OFFSET = 0x25862
WARP_ZONE_START_Y_OFFSET = 0x1710
WARP_ZONE_MOTION_FLAGS_OFFSET = 0x1716
WARP_ZONE_LEVEL_MAPPING_OFFSET = 0x2583a
MOTION_FLAG_MAPPINGS = { 0x24: 'stationary', 0x28: 'falling' }
PIXELS_PER_TILE = 16

# Tile mappings
TILES = [('empty', ' '),
         ('crack1', 'X'),
         ('door', '#'),
         ('girder_block', '='),
         ('jetpack', 'J'),
         ('bluewall', '#'),
         ('fire1', 'W'),
         ('fire2', 'W'),
         ('fire3', 'W'),
         ('fire4', 'W'),
         ('trophy1', 'T'),
         ('trophy2', 'T'),
         ('trophy3', 'T'),
         ('trophy4', 'T'),
         ('trophy5', 'T'),
         ('pipe_horiz', '>'),
         ('pipe_vert', 'V'),
         ('redwall', '#'),
         ('crack2', 'X'),
         ('bluetile', '%'),
         ('gun', 'G'),
         ('diag1', '\\'),
         ('diag2', '/'),
         ('diag3', '\\'),
         ('diag4', '/'),
         ('tent1', 'W'),
         ('tent2', 'W'),
         ('tent3', 'W'),
         ('tent4', 'W'),
         ('girder_vert', '|'),
         ('girder_horiz1', '-'),
         ('girder_horiz2', '-'),
         ('low_grass', '_'),
         ('trunk', '|'),
         ('branch1', 'O'),
         ('branch2', 'O'),
         ('water1', 'o'),
         ('water2', 'o'),
         ('water3', 'o'),
         ('water4', 'o'),
         ('water5', 'o'),
         ('stars', '.'),
         ('moon', '.'),
         ('branch3', 'O'),
         ('branch4', 'O'),
         ('branch5', 'O'),
         ('branch6', 'O'),
         ('diamond_blue', '$'),
         ('purple_dot', '*'),
         ('diamond_red', '$'),
         ('crown', 'M'),
         ('ring', 'Q'),
         ('septer', '&'), 
         ('dave1', 'D'),
         ('dave2', 'D'),
         ('dave3', 'D'),
         ('dave4', 'D'),
         ('dave5', 'D'),
         ('dave6', 'D'),
         ('dave7', 'D'),
         ('shadow1', ' '),
         ('shadow2', ' '),
         ('shadow3', ' '),
         ('shadow4', ' '),
         ('shadow5', ' '),
         ('shadow6', ' '),
         ('shadow7', ' '),
         ('jump_right', 'D'),
         ('jump_left', 'D'),
         ('shadow_right', ' '),
         ('shadow_left', ' '),
         ('climb1', 'D'),
         ('climb2', 'D'),
         ('climb3', 'D'),
         ('shadow_climb1', ' '),
         ('shadow_climb2', ' '),
         ('shadow_climb3', ' '),
         ('jetpack_right1', 'D'),
         ('jetpack_right2', 'D'),
         ('jetpack_right3', 'D'),
         ('jetpack_left1', 'D'),
         ('jetpack_left2', 'D'),
         ('jetpack_left3', 'D'),
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
         ('green_ball1', 'g'),
         ('green_ball2', 'g'),
         ('green_ball3', 'g'),
         ('green_ball4', 'g'),
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

def pixel_to_tile_coord_x(p):
    """
        Translates pixel numbers to a tile X cooredinate.
    """

    # Return the result
    return p // PIXELS_PER_TILE

def pixel_to_tile_coord_y(p):
    """
        Translates pixel numbers to a tile Y cooredinate.
    """

    # Return the result
    return (p // PIXELS_PER_TILE) - 1 

class WarpZoneInfo(object):
    """
        Represents Warp Zone information.
    """

    @staticmethod
    def parse(bin_bytes):
        """
            Parses all the warp zones from the binary bytes.
            Returns None for levels that do not have warp-zones.
        """

        # Extract per-level warp zone data 
        warp_zone_level_data_fmt = '<%dH%dH' % (NORMAL_LEVELS_NUM, NORMAL_LEVELS_NUM)
        warp_zone_level_data = struct.unpack(warp_zone_level_data_fmt, bin_bytes[WARP_ZONE_LEVELS_DATA_OFFSET:WARP_ZONE_LEVELS_DATA_OFFSET + struct.calcsize(warp_zone_level_data_fmt)])

        # Extract the global data for warp zones
        warp_zone_start_y = pixel_to_tile_coord_y(struct.unpack('<H', bin_bytes[WARP_ZONE_START_Y_OFFSET:WARP_ZONE_START_Y_OFFSET + struct.calcsize('<H')])[0])
        warp_zone_init_motion = MOTION_FLAG_MAPPINGS[struct.unpack('<H', bin_bytes[WARP_ZONE_MOTION_FLAGS_OFFSET:WARP_ZONE_MOTION_FLAGS_OFFSET + struct.calcsize('<H')])[0]]

        # Extract warp-level mapping
        warp_zone_mappings_fmt = '<%dH' % (NORMAL_LEVELS_NUM,)
        warp_mappings = struct.unpack(warp_zone_mappings_fmt, bin_bytes[WARP_ZONE_LEVEL_MAPPING_OFFSET:WARP_ZONE_LEVEL_MAPPING_OFFSET + struct.calcsize(warp_zone_mappings_fmt)])
        
        # Return all parsed warp zones
        zones = []
        for i in range(NORMAL_LEVELS_NUM):
            horiz_scroll = warp_zone_level_data[NORMAL_LEVELS_NUM + i]
            if horiz_scroll == 0:
                zones.append(None)
            else:
                zones.append(WarpZoneInfo(pixel_to_tile_coord_x(horiz_scroll) + warp_zone_level_data[i], warp_zone_start_y, warp_zone_init_motion, warp_mappings[i]))
        return zones

    def __init__(self, startx, starty, init_motion, warp_level):
        """
            Initializes.
        """

        # Saves data
        self.startx = startx
        self.starty = starty
        self.init_motion = init_motion
        self.warp_level = warp_level

    def __str__(self):
        """
            Returns a nice text-representation of the warp-zone information.
        """

        # Build the warp zone information
        return 'Warp zone mapped to level %d starts at (%d, %d) while %s.' % (self.warp_level, self.startx, self.starty, self.init_motion)

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
        levels = [ Level(bin_bytes[SPECIAL_LEVEL_OFFSET:SPECIAL_LEVEL_OFFSET + SPECIAL_LEVEL_SIZE], 'Intro screen') ]

        # Parse initial state for all normal levels
        init_states_fmt = '<%dB%dH%dH' % (NORMAL_LEVELS_NUM, NORMAL_LEVELS_NUM, NORMAL_LEVELS_NUM)
        init_states = struct.unpack(init_states_fmt, bin_bytes[NORMAL_LEVELS_INIT_STATE_OFFSET:NORMAL_LEVELS_INIT_STATE_OFFSET + struct.calcsize(init_states_fmt)])

        # Parse warp zones for normal levels
        warp_zones = WarpZoneInfo.parse(bin_bytes)

        # Parse normal levels
        for i in range(NORMAL_LEVELS_NUM):
            data = bin_bytes[NORMAL_LEVELS_OFFSET + (NORMAL_LEVELS_SIZE*i):NORMAL_LEVELS_OFFSET + NORMAL_LEVELS_SIZE*(i+1)]
            init_motion, startx, starty = init_states[i], pixel_to_tile_coord_x(init_states[NORMAL_LEVELS_NUM + i]), pixel_to_tile_coord_y(init_states[2*NORMAL_LEVELS_NUM + i])
            levels.append(Level(data, 'Level %d' % (i+1,), startx, starty, MOTION_FLAG_MAPPINGS[init_motion], warp_zones[i]))

        # Parse the buggy level
        levels.append(Level(bin_bytes[BUGGY_LEVEL_OFFSET:BUGGY_LEVEL_OFFSET + BUGGY_LEVEL_SIZE], 'Buggy warp level'))

        # Return all the levels
        return levels

    @staticmethod
    def get_tile(index):
        """
            Return the tile representation.
        """

        # Default representatiob of unknown tiles
        if len(TILES) <= index:
            return '?'
        return TILES[index][1]

    def __init__(self, level_bytes, level_title, startx=0, starty=0, init_motion=None, warp_zone=None):
        """
            Initializes.
        """

        # Handle level data
        if len(level_bytes) == 1280:
            self.path_data = level_bytes[:256]
            self.tiles = level_bytes[256:-24]
            self.width = 100
            self.height = 10
        elif len(level_bytes) == 70:
            self.path_data = b''
            self.tiles = level_bytes[:]
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
        
        # Save the text representation ahead-of-time
        self.repr = self.title + ':\n\n' + '\n'.join([ ''.join([ Level.get_tile(tile) for tile in self.tiles[i:i+self.width] ]) for i in range(0, len(self.tiles), self.width) ])
        if self.warp_zone is not None:
            self.repr += '\n\n%s' % (self.warp_zone,)

    def __str__(self):
        """
            Returns a nice string-representation of the level.
        """

        # Return the text representation
        return self.repr

def main():
    """
        Main functionality.
    """

    # Parse DAVE.EXE
    with open('DAVE.EXE', 'rb') as f:
        contents = f.read()

    # Parse levels
    levels = Level.parse(contents)

    # Handle menu
    while True:
        print('Loaded %d levels.' % (len(levels)))
        choice = input('Choose a level to view (zero-based) or \'Q\' to quit: ')
        if choice.isdigit():
            level_num = int(choice)
            if level_num < 0 or level_num >= len(levels):
                print('Invalid level number')
                continue
            clear_screen()
            print(levels[level_num])
            print('\n\n')
        elif choice.upper() == 'Q':
            print('Quitting.')
            break
        else:
            print('Invalid option.\n')

if __name__ == '__main__':
    main()

