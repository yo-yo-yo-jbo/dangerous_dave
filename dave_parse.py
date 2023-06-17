#!/usr/bin/env python3
import struct
import binascii
import string
import os

# Fine-tunables
NORMAL_LEVELS_OFFSET = 0x26E0A
NORMAL_LEVELS_SIZE = 0x500
NORMAL_LEVELS_NUM = 10
NORMAL_LEVELS_INIT_STATE_OFFSET = 0x257E8
SPECIAL_LEVEL_OFFSET = 0x25EA4
SPECIAL_LEVEL_SIZE = 70
WARP_ZONE_LEVELS_DATA_OFFSET = 0x25862
WARP_ZONE_START_Y_OFFSET = 0x1710
WARP_ZONE_MOTION_FLAGS_OFFSET = 0x1716
MOTION_FLAG_MAPPINGS = { 0x24: 'stationary', 0x28: 'falling' }
PIXELS_PER_TILE = 16

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

        # Return all parsed warp zones
        zones = []
        for i in range(NORMAL_LEVELS_NUM):
            horiz_scroll = warp_zone_level_data[NORMAL_LEVELS_NUM + i]
            if horiz_scroll == 0:
                zones.append(None)
            else:
                zones.append(WarpZoneInfo(pixel_to_tile_coord_x(horiz_scroll) + warp_zone_level_data[i], warp_zone_start_y, warp_zone_init_motion))
        return zones

    def __init__(self, startx, starty, init_motion):
        """
            Initializes.
        """

        # Saves data
        self.startx = startx
        self.starty = starty
        self.init_motion = init_motion

    def __str__(self):
        """
            Returns a nice text-representation of the warp-zone information.
        """

        # Build the warp zone information
        return 'Warp zone starts at (%d, %d) while %s.' % (self.startx, self.starty, self.init_motion)

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

        # Return all the levels
        return levels

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
            self.title = '%s (start at (%d, %d) %s)' % (level_title, startx, starty, init_motion)
        elif len(level_bytes) == 70:
            self.path_data = b''
            self.tiles = level_bytes[:]
            self.width = 10
            self.height = 7
            self.title = level_title
        else:
            raise Exception('Invalid level length %d' % (len(level_bytes),))

        # Save warp zone (might be None)
        self.warp_zone = warp_zone

        # Map tiles to printable characters
        mapping = {}
        mapping[0] = ' '
        potentials = [ l for l in string.ascii_letters ]
        #potentials = [ i for i in string.printable if i not in string.whitespace ]
        for tile in self.tiles:
            if tile in mapping:
                continue
            mapping[tile] = potentials.pop()
        
        # Save the text representation ahead-of-time
        self.repr = self.title + ':\n\n' + '\n'.join([ ''.join([ mapping[tile] for tile in self.tiles[i:i+self.width] ]) for i in range(0, len(self.tiles), self.width) ])
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

