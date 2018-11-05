#!/usr/bin/python3
import tensorflow as tf 
from tensorflow import keras
# Helper libraries
import numpy as np 
import pandas as pd
from functools import reduce
import json

def pad_list_with_zeros(input_list, desired_length):
    assert(desired_length >= len(input_list))
    pad = [0] * (desired_length - len(input_list))
    return list(map(int, input_list + pad))

def flatten(l):
    return reduce(lambda x,y: x+y, l, [])

def abs_list(l):
    return list(map(lambda x: abs(x), l))

def get_complete_meld_list(meld_list):
    ml = list(map(lambda x: pad_list_with_zeros(x, 4), meld_list)) # Every meld now has size 4
    ml = flatten(ml)
    ml = abs_list(ml)
    ml = pad_list_with_zeros(ml, 16)

    return ml

def normalize_tiles(tile_list):
    normalize_funtion = lambda x : abs(x // 4 + 1)
    return list(map(normalize_funtion, list(map(int, tile_list))))


def discard_predicted_tile(current_game_state):
    discards = []
    for i in range(0,4):
        discards.append(current_game_state['Discards_' + str(i)])

    melds = []
    for i in range(0, 4):
        m = current_game_state['Melds_' + str(i)]
        m = list(map(lambda xs: xs[:-1], m)) # remove the player who gave you the tile
        melds.append(m)
        
    riichi = current_game_state['Riichi']

    self_closed_hand = current_game_state['Hand']
    self_closed_hand.sort()
    dora_indicators = current_game_state['Dora']

    wind = current_game_state['Seat']

    # DORA[1-5], Wind, Riichi[1-4], Tiles[1-14], P1Discards[1-29], P2Discards[1-29], P3Discards[1-29], P4discards[1-29], P1Melds, P2Melds, P3Melds, P4Melds
    # Input size: 204

    # game_status = dora_indicators + [wind] + riichi + self_closed_hand + discards[0] + discards[1] + discards[2] + discards[3] + melds[0] + melds[1] + melds[2] + melds[3]
    game_status = pad_list_with_zeros(normalize_tiles(dora_indicators), 5) + [wind] + pad_list_with_zeros(riichi, 4) + pad_list_with_zeros(normalize_tiles(self_closed_hand), 14) + pad_list_with_zeros(normalize_tiles(discards[0]), 29) + pad_list_with_zeros(normalize_tiles(discards[1]), 29) + pad_list_with_zeros(normalize_tiles(discards[2]), 29) + pad_list_with_zeros(normalize_tiles(discards[3]), 29) + get_complete_meld_list(melds[0]) + get_complete_meld_list(melds[1]) + get_complete_meld_list(melds[2]) + get_complete_meld_list(melds[3])
    game_status = [game_status]
    game_status = np.asarray(game_status)

    print(type(game_status), len(game_status[0]))
    print(game_status)

    model = keras.models.load_model('training/training/discard_model.h5')
    prediction = model.predict(game_status)
    index = np.argmax(prediction) # Predicted tile
    res = {"Discard" : self_closed_hand[index]}
    print(res)

if __name__=='__main__':

    state_sample = {'Riichi': [],
                  'Discards_0': [101, 89],
                  'Melds_0': [],
                  'Discards_1': [14, 4],
                  'Melds_1': [],
                  'Discards_2': [37, 65],
                  'Melds_2': [],
                  'Discards_3': [76],
                  'Melds_3': [[56, 62, -65, 2]],
                  'Hand': [22, 23, 45, 47, 53, 58, 61, 68, 87, 103, 111, 118, 133],
                  'Remaining': 76,
                  'Dora': [104],
                  'Seat': 0}


    print(state_sample['Hand'])
    discard_predicted_tile(state_sample)