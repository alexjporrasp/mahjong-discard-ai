import xml.etree.ElementTree as et
import re
import os
from meld import Meld
from player import Player
from round import Round

# filename = '../log-content/2018081700gm-00e1-0000-7edc4c05.xml'

def get_complete_meld_list(meld_list):
    res = []
    for meld in meld_list:
        for tile in meld:
            res.append(int(tile) // 4 + 1)
        if len(meld) < 4:
            res.append(0)

    if len(res) < 16:
        for i in range(0, 16-len(res)):
            res.append(0)

    return res

def from_list_to_str(list_input):
    res = ''
    for item in list_input:
        if (res != ''):
            res += ', '
        res += str(item)

    return res


def pad_list_with_zeros(input_list, desired_length):
    assert(desired_length >= len(input_list))
    pad = [0] * (desired_length - len(input_list))
    return list(map(int, input_list + pad))

def get_file_header():
    header_str = ''

    header_str = 'DORA1, DORA2, DORA3, DORA4, DORA5, Wind, R1, R2, R3, R4'

    for i in range(1, 15):
        header_str += ', T' + str(i)

    for i in range(1, 30):
        header_str += ', ' + 'P1D' + str(i)
    
    for i in range(1, 30):
        header_str += ', ' + 'P2D' + str(i)

    for i in range(1, 30):
        header_str += ', ' + 'P3D' + str(i)

    for i in range(1, 30):
        header_str += ', ' + 'P4D' + str(i)

    for i in range(1, 5):
        for j in range(1, 5):
            header_str += ', ' + 'P1M' + str(i) + '_' + str(j)

    for i in range(1, 5):
        for j in range(1, 5):
            header_str += ', ' + 'P2M' + str(i) + '_' + str(j)

    for i in range(1, 5):
        for j in range(1, 5):
            header_str += ', ' + 'P3M' + str(i) + '_' + str(j)

    for i in range(1, 5):
        for j in range(1, 5):
            header_str += ', ' + 'P4M' + str(i) + '_' + str(j)

    header_str += ', Discard\n'

    return header_str

def normalize_tiles(tile_list):
    normalize_funtion = lambda x : x // 4 + 1
    return list(map(normalize_funtion, list(map(int, tile_list))))

def parse_log_xml(xml_filename, output_filepath):
    tree = et.parse(xml_filename)
    root = tree.getroot()
    cur_round = []

    out_file = open(output_filepath, 'a+')

    # We check whether the file is empty

    if (os.stat(output_filepath).st_size == 0):
        print("File is empty. Writing header...")
        # Generate header
        # The input part of the classifier consists of the player's hand, the opponents' discarded tiles and open melds
        # The output of the classifier is the tile to discard
        out_file.write(get_file_header())
    
    # print('Reading ' + xml_filename)

    for child in root:
        if (child.tag == 'INIT'):
            cur_round = Round(child.attrib['seed'].split(',')[5])
            cur_round.init_player(child.attrib['hai0'].split(','), ((0 - int(child.attrib['oya'])) + 4) % 4)
            cur_round.init_player(child.attrib['hai1'].split(','), ((1 - int(child.attrib['oya'])) + 4) % 4)
            cur_round.init_player(child.attrib['hai2'].split(','), ((2 - int(child.attrib['oya'])) + 4) % 4)
            cur_round.init_player(child.attrib['hai3'].split(','), ((3 - int(child.attrib['oya'])) + 4) % 4)

        if (re.compile('T[0-9]+').match(child.tag)):
            # Player 1 draws a tile
            cur_round.player[0].draw_tile(child.tag[1:])

        if (re.compile('U[0-9]+').match(child.tag)):
            # Player 2 draws a tile
            cur_round.player[1].draw_tile(child.tag[1:])

        if (re.compile('V[0-9]+').match(child.tag)):
            # Player 3 draws a tile
            cur_round.player[2].draw_tile(child.tag[1:])

        if (re.compile('W[0-9]+').match(child.tag)):
            # Player 4 draws a tile
            cur_round.player[3].draw_tile(child.tag[1:])

        if (re.compile('D[0-9]+').match(child.tag)):
            # Player 1 discards a tile
            # print('hand: ', cur_round.player_one_hand, ' p2 discards: ', cur_round.player_two_discards, ' p3 disards: ', cur_round.player_three_discards, ' p4 discards: ', cur_round.player_four_discards, 'discard: ', child.tag[1:])
            str_res = from_list_to_str(pad_list_with_zeros(normalize_tiles(cur_round.dora), 5) + [cur_round.player[0].wind] + [cur_round.player[0].declared_riichi] + [cur_round.player[1].declared_riichi] + [cur_round.player[2].declared_riichi] + [cur_round.player[3].declared_riichi] + pad_list_with_zeros(normalize_tiles(cur_round.player[0].closed_hand), 14) + pad_list_with_zeros(normalize_tiles(cur_round.player[0].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[1].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[2].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[3].discards), 29) + get_complete_meld_list(cur_round.player[0].melds) + get_complete_meld_list(cur_round.player[1].melds) + get_complete_meld_list(cur_round.player[2].melds) + get_complete_meld_list(cur_round.player[3].melds))
            str_res += ', ' + str(cur_round.player[0].closed_hand.index(int(child.tag[1:]))) + '\n'
            out_file.write(str_res)
         
            cur_round.player[0].discard_tile(child.tag[1:])

        if (re.compile('E[0-9]+').match(child.tag)):
            # Player 2 discards a tile
            # print('hand: ', cur_round.player_two_hand, ' p1 discards: ', cur_round.player_one_discards, ' p3 disards: ', cur_round.player_three_discards, ' p4 discards: ', cur_round.player_four_discards, ' discard: ', child.tag[1:])
            
            str_res = from_list_to_str(pad_list_with_zeros(normalize_tiles(cur_round.dora), 5) + [cur_round.player[1].wind] + [cur_round.player[0].declared_riichi] + [cur_round.player[1].declared_riichi] + [cur_round.player[2].declared_riichi] + [cur_round.player[3].declared_riichi] + pad_list_with_zeros(normalize_tiles(cur_round.player[1].closed_hand), 14) + pad_list_with_zeros(normalize_tiles(cur_round.player[0].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[1].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[2].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[3].discards), 29) + get_complete_meld_list(cur_round.player[0].melds) + get_complete_meld_list(cur_round.player[1].melds) + get_complete_meld_list(cur_round.player[2].melds) + get_complete_meld_list(cur_round.player[3].melds))
            str_res += ', ' + str(cur_round.player[1].closed_hand.index(int(child.tag[1:]))) + '\n'
            out_file.write(str_res)
            cur_round.player[1].discard_tile(child.tag[1:])

        if (re.compile('F[0-9]+').match(child.tag)):
            # Player 3 discards a tile
            # print('hand: ', cur_round.player_three_hand, ' p1 discards: ', cur_round.player_one_discards, ' p2 disards: ', cur_round.player_two_discards, ' p4 discards: ', cur_round.player_four_discards, ' discard: ', child.tag[1:])
            str_res = from_list_to_str(pad_list_with_zeros(normalize_tiles(cur_round.dora), 5) + [cur_round.player[2].wind] + [cur_round.player[0].declared_riichi] + [cur_round.player[1].declared_riichi] + [cur_round.player[2].declared_riichi] + [cur_round.player[3].declared_riichi] + pad_list_with_zeros(normalize_tiles(cur_round.player[2].closed_hand), 14) + pad_list_with_zeros(normalize_tiles(cur_round.player[0].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[1].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[2].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[3].discards), 29) + get_complete_meld_list(cur_round.player[0].melds) + get_complete_meld_list(cur_round.player[1].melds) + get_complete_meld_list(cur_round.player[2].melds) + get_complete_meld_list(cur_round.player[3].melds))
            str_res += ', ' + str(cur_round.player[2].closed_hand.index(int(child.tag[1:]))) + '\n'
            out_file.write(str_res)
            cur_round.player[2].discard_tile(child.tag[1:])

        if (re.compile('G[0-9]+').match(child.tag)): 
            # Player 4 discards a tile
            # print('hand: ', cur_round.player_four_hand, ' p1 discards: ', cur_round.player_one_discards, ' p2 disards: ', cur_round.player_two_discards, ' p3 discards: ', cur_round.player_three_discards, ' discard: ', child.tag[1:])
            str_res = from_list_to_str(pad_list_with_zeros(normalize_tiles(cur_round.dora), 5) + [cur_round.player[3].wind] + [cur_round.player[0].declared_riichi] + [cur_round.player[1].declared_riichi] + [cur_round.player[2].declared_riichi] + [cur_round.player[3].declared_riichi] + pad_list_with_zeros(normalize_tiles(cur_round.player[3].closed_hand), 14) + pad_list_with_zeros(normalize_tiles(cur_round.player[0].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[1].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[2].discards), 29) + pad_list_with_zeros(normalize_tiles(cur_round.player[3].discards), 29) + get_complete_meld_list(cur_round.player[0].melds) + get_complete_meld_list(cur_round.player[1].melds) + get_complete_meld_list(cur_round.player[2].melds) + get_complete_meld_list(cur_round.player[3].melds))
            str_res += ', ' + str(cur_round.player[3].closed_hand.index(int(child.tag[1:]))) + '\n'
            out_file.write(str_res)
            cur_round.player[3].discard_tile(child.tag[1:])

        if (child.tag == 'N'):
            open_meld = Meld.decode(child.attrib['m'])
            melded_tiles = open_meld.tiles
            cur_round.player[int(child.attrib['who'])].meld(list(melded_tiles))
          
        if (child.tag == 'REACH'):
            cur_round.player[int(child.attrib['who'])].declare_riichi()

        if (child.tag == 'DORA'):
            cur_round.add_dora(child.attrib['hai'])
    out_file.close()

if __name__=='__main__':
    import sys
    import bz2
    import sqlite3

    parse_log_xml(sys.argv[1], sys.argv[2])