import script_parser
import sys
import os

if __name__=='__main__':
    game_log_directory = sys.argv[1]
    counter = 0
    for filename in os.listdir(game_log_directory):
        if (counter > len(os.listdir(game_log_directory)) * .8):
            script_parser.parse_log_xml(game_log_directory + '/' + filename, 'test_data.csv')  
        else:
            script_parser.parse_log_xml(game_log_directory + '/' + filename, 'train_data.csv')
        counter += 1
        # print(str(counter), '/', len(os.listdir(game_log_directory)))
    