import pandas as pd
import numpy as np
from divide_data import divide_data_by_contrast, divide_data_by_flow_direction
from preprocess import omr_preprocess

if __name__ == "__main__":
    path_to_data = input('PATH TO DATA: ')
    data = pd.read_csv(path_to_data)
    data.columns = ['X_coord', 'Y_coord', 'heading_direction', \
                'cumulative_direction','beat_freq', 'beat_amp', \
                'tail_move?', 'timestamp', 'contrast_level', 'flow_direction']
    right, left = divide_data_by_flow_direction(data)
    right_C0, right_C01, right_C1, right_C2, right_C3, right_C5, right_C7, right_C10 = divide_data_by_contrast(right)
    left_C0, left_C01, left_C1, left_C2, left_C3, left_C5, left_C7, left_C10 = divide_data_by_contrast(left)
    preproc_left_C01 = omr_preprocess(left_C01)
    print('This is the preprocessed left_C01: \n',preproc_left_C01)
    print('Successful data division')
