import pandas as pd

def divide_data_by_flow_direction(data):
    right = pd.DataFrame(data[data.flow_direction == 1])
    left = pd.DataFrame(data[data.flow_direction == 2])
    return right, left

def divide_data_by_contrast(data):
    C_0 = pd.DataFrame(data[data.contrast_level == 0])
    C_01 = pd.DataFrame(data[data.contrast_level == 0.01])
    C_1 = pd.DataFrame(data[data.contrast_level == 0.1])
    C_2 = pd.DataFrame(data[data.contrast_level == 0.2])
    C_3 = pd.DataFrame(data[data.contrast_level == 0.3])
    C_5 = pd.DataFrame(data[data.contrast_level == 0.5])
    C_7 = pd.DataFrame(data[data.contrast_level == 0.7])
    C_10 = pd.DataFrame(data[data.contrast_level == 1])
    return C_0, C_01, C_1, C_2, C_3, C_5, C_7, C_10


if __name__ == "__main__":
    path_to_data = '/Users/katarzynakupczyk/msci_dissertation_2022/dissertation2022/raw_data/xy_hc_fai_tstp2.csv'
    data = pd.read_csv(path_to_data)
    data.columns = ['X_coord', 'Y_coord', 'heading_direction', \
                'cumulative_direction','beat_freq', 'beat_amp', \
                'tail_move?', 'timestamp', 'contrast_level', 'flow_direction']
    right, left = divide_data_by_flow_direction(data)
    right_C0, right_C01, right_C1, right_C2, right_C3, right_C5, right_C7, right_C10 = divide_data_by_contrast(right)
    left_C0, left_C01, left_C1, left_C2, left_C3, left_C5, left_C7, left_C10 = divide_data_by_contrast(left)
    print('Successful data division')
