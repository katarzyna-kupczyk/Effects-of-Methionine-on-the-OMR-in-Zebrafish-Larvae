import pandas as pd
import numpy as np
from scipy import interpolate
from divide_data import divide_data_by_contrast
from divide_data import divide_data_by_flow_direction


def omr_preprocess(data):
    # remove timestamp and extras
    # keep x, y, heading, cumulative, timestamp
    new = data.drop(columns = ['beat_freq', 'beat_amp','tail_move?','contrast_level','flow_direction'])


    # resetting index
    new = pd.DataFrame(new)
    new = new.set_index('timestamp').reset_index()


    # remove time points where there was an angle change of more than pi from one frame to another
    for row in range(len(new)-1):
        heading = new.iloc[row,3]
        next_heading = new.iloc[row+1,3]
        if np.abs(next_heading-heading) >= np.pi:
            new.iloc[row+1,3] = new.iloc[row,3]


    # interpolating and normalising data to a fixed set of points
    interp = pd.DataFrame(columns=['timestamp','X_coord','Y_coord','heading_direction','cumulative_direction'])
    for column in new.columns:
        x = np.arange(0,len(new))
        y = new[column]
        f = interpolate.interp1d(x,y)

        x_new = np.arange(0,3000,1)
        y_new = f(x_new)
        interp[column] = y_new


    # setting first cumulative_angle to zero and ajdusting all others
    interp.iloc[:,4] -= interp.iloc[0,4]


    # calculating distance traveled between each timeframe
    # distance = sqrt((x2-x1)**2 + (y2-y1)**2)
    interp['distance_pts'] = 0
    for row in range(1,len(interp),1):
        distance = np.sqrt((interp['X_coord'][row]-interp['X_coord'][row-1])**2\
                            +(interp['Y_coord'][row]-interp['Y_coord'][row-1])**2)
        interp.iloc[row,5] = distance


    # cleaning the timestamps
    interp.insert(0, 'new_timestamp', range(1, 1 + len(interp)))
    interp = interp.drop(columns=['timestamp']).rename(columns={'new_timestamp':'timestamp'})
    interp['timestamp'] = interp['timestamp']/1000

    return np.array(interp)

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
