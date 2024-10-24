#!/usr/bin/env python3
import struct
import os
import colorama

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
        levels = [ Level(bin_bytes[SPECIAL_LEVEL_OFFSET:SPECIAL_LEVEL_OFFSET + SPECIAL_LEVEL_SIZE], 'Intro screen', SPECIAL_LEVEL_OFFSET) ]

        # Parse initial state for all normal levels
        init_states_fmt = '<%dB%dH%dH' % (NORMAL_LEVELS_NUM, NORMAL_LEVELS_NUM, NORMAL_LEVELS_NUM)
        init_states = struct.unpack(init_states_fmt, bin_bytes[NORMAL_LEVELS_INIT_STATE_OFFSET:NORMAL_LEVELS_INIT_STATE_OFFSET + struct.calcsize(init_states_fmt)])

        # Parse warp zones for normal levels
        warp_zones = WarpZoneInfo.parse(bin_bytes)

        # Parse normal levels
        for i in range(NORMAL_LEVELS_NUM):
            data = bin_bytes[NORMAL_LEVELS_OFFSET + (NORMAL_LEVELS_SIZE*i):NORMAL_LEVELS_OFFSET + NORMAL_LEVELS_SIZE*(i+1)]
            init_motion, startx, starty = init_states[i], pixel_to_tile_coord_x(init_states[NORMAL_LEVELS_NUM + i]), pixel_to_tile_coord_y(init_states[2*NORMAL_LEVELS_NUM + i])
            levels.append(Level(data, 'Level %d' % (i+1,), NORMAL_LEVELS_OFFSET + (NORMAL_LEVELS_SIZE*i), startx, starty, MOTION_FLAG_MAPPINGS[init_motion], warp_zones[i]))

        # Parse the buggy warp zone level
        levels.append(Level(bin_bytes[BUGGY_LEVEL_OFFSET:BUGGY_LEVEL_OFFSET + BUGGY_LEVEL_SIZE], 'Buggy warp level', BUGGY_LEVEL_OFFSET))

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

    def __init__(self, level_bytes, level_title, tiles_offset, startx=0, starty=0, init_motion=None, warp_zone=None):
        """
            Initializes.
        """

        # Handle level data
        if len(level_bytes) == 1280:
            self.path_data = level_bytes[:256]
            self.tiles = [ tile for tile in level_bytes[256:-24] ]
            self.width = 100
            self.height = 10
            self.tiles_offset = tiles_offset + 256
        elif len(level_bytes) == 70:
            self.path_data = b''
            self.tiles = [ tile for tile in level_bytes[:] ]
            self.width = 10
            self.height = 7
            self.tiles_offset = tiles_offset
        else:
            raise Exception('Invalid level length %d' % (len(level_bytes),))

        # Save the title
        if init_motion is not None:
            self.title = '%s (start at (%d, %d) %s)' % (level_title, startx, starty, init_motion)
        else:
            self.title = level_title

        # Save warp zone (might be None)
        self.warp_zone = warp_zone
        
    def __str__(self):
        """
            Returns a nice string-representation of the level.
        """
        
        # Returns the text representation
        self_repr = self.title + ':\n\n' + '\n'.join([ ''.join([ Level.get_tile(tile) for tile in self.tiles[i:i+self.width] ]) for i in range(0, len(self.tiles), self.width) ])
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

def main():
    """
        Main functionality.
    """

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
    saved = True
    while True:

        # Handle all exceptions
        try:

            # Present header
            print('Loaded %d levels.' % (len(levels)))
            print('Current intro title: "%s".' % (titles[0],))
            print('Current intro subtitle: "%s".' % (titles[1],))
            if not saved:
                print('You have UNSAVED edits.\n')
            print('Menu:\n\t[V]iew a level.\n\t[E]dit a level.\n\tEdit intro [T]itle.\n\tEdit intro su[B]title.\n\t[S]ave pending changes.\n\t[Q]uit without saving.')
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
                    raise Exception('Nothing to save.')
                choice = input('This will completely override file %s! Choose \'Y\' to do it or any key to cancel: ' % (FILENAME,)).upper()
                if choice != 'Y':
                    continue
                new_bytes = bin_bytes[:]
                for level in levels:
                    new_bytes = new_bytes[:level.tiles_offset] + bytes(level.tiles) + new_bytes[level.tiles_offset + len(level.tiles):]
                new_bytes = new_bytes[:TITLE_OFFSET] + titles[0].encode() + new_bytes[TITLE_OFFSET + TITLE_SIZE:]
                new_bytes = new_bytes[:SUBTITLE_OFFSET] + titles[1].encode() + new_bytes[SUBTITLE_OFFSET + SUBTITLE_SIZE:]
                with open(FILENAME, 'wb') as f:
                    f.write(new_bytes)
                clear_screen()
                print('Written %d bytes to file %s successfully.' % (len(bin_bytes), FILENAME))
                saved = True
                continue

            # Handle quitting
            if choice == 'Q':
                if not saved:
                    choice = input('All your changed will be lost! Choose \'Y\' to quit or any key to cancel: ').upper()
                    if choice != 'Y':
                        continue
                print('Quitting.\n')
                break
            
            # Default handling
            raise Exception('Invalid option: %s\n' % (choice,))

        # Handle exceptions
        except Exception as ex:
            clear_screen()
            print(ex)


if __name__ == '__main__':
    main()

