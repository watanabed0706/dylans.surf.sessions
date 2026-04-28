import json
import pandas as pd
import sys

SESH = "./data/this_sesh.json"
CLIPS = "./data/clips.txt"
GPMF = "./data/gpmf.json"

def read_json():
    with open(GPMF, 'r') as f:
        return json.load(f)

def print_stuff(data):
    print(data["1"]["streams"].keys())

def write_to_demo(data):
    with open("demofile.txt", "w") as f:
        for sample in data["1"]["streams"]["ACCL"]["samples"]:
            x = str(sample)
            f.write(x+'\n')

def accl_df(data):
    df = pd.DataFrame(data["1"]["streams"]["ACCL"]["samples"])
    df[['z', 'x', 'y']] = pd.DataFrame(df['value'].tolist(), index=df.index)
    df['second'] = df.index/200
    df['second'] = df['second'].astype('int')
    df['dwn-fwd'] = ((df['y']+1.2) - (df['z']-9.81))
    return df

def get_timestamps(df):
    key_seconds = list(df[
        (df.z <  1) & # High Z = GoPro is upright or Rising
        (df.z > -1) & # Low  Z = GoPro is upsidedown or Falling
        (df.y <  3) & # High Y = GoPro is Lens-Down or Moving Backwards
        (df.y > -5) & # Low  Y = GoPro is Lens-Up or Moving Foward
        (df.x <  5) & # High X = GoPro is right-side-down or rotating left
        (df.x > -5)   # High X = GoPro is left-side-down or rotating right
        ]['second'].unique())
    length = 0
    starts = []
    ends = []
    for i in range(len(key_seconds)):
        
        if(i < len(key_seconds)-1):
            diff = key_seconds[i+1] - key_seconds[i]
        else:
            diff = 10000
        
        if (diff < 4):
            if (length == 0):
                starts.append(key_seconds[i])
            length += diff
        else:
            if(length > 0):
                ends.append(key_seconds[i])
                length = 0
    # print(sys.argv[1]+str(starts)+str(ends))
    return [starts,ends]

def filter_em(starts,ends):
    for i in range(len(starts)):
        if ((ends[i] - starts[i]) <= 5):
            starts.pop(i)
            ends.pop(i)
            starts,ends = filter_em(starts,ends)
            break
    return(starts,ends)

def join_em(starts,ends):
    for i in range(len(starts)-1):
        if(starts[i+1]-ends[i] <= 14):
            starts.pop(i+1)
            ends[i] = ends.pop(i+1)
            starts,ends = join_em(starts,ends)
            break
    return (starts,ends)

def buffer_em(starts,ends,max):
    for i in range(len(starts)):
        if(starts[i] <= 5):
            starts[i] = 0
        else:
            starts[i] -= 5
        if(ends[i]+5 >= max):
            ends[i] = max
        else:
            ends[i] += 5
    return (starts,ends)

def add_to_clips_file(starts,ends):
    with open(CLIPS, "a") as f:

        for i in range(len(starts)):
            f.write("file \'"+sys.argv[1][:-11]+"X"+
            sys.argv[1][-10:-3]+"MP4"+'\'\n'+
            "inpoint "+str(starts[i])+'\n'+
            "outpoint "+str(ends[i])+"\n\n")

def add_to_thumbnais_file(starts,ends):
    diffs = [ends[i] - starts[i] for i in range(len(starts))]
    best_index = diffs.index(max(diffs))
    thumbnail_frame = round(starts[best_index] + (diffs[best_index]*.65))

def add_best(starts,ends):
    if(starts):
        inpoint, outpoint = max(zip(starts, ends), key=lambda x: x[1] - x[0])
        wavetime = outpoint - inpoint
        if (wavetime >= 60):
            inpoint += ((wavetime - 60)/2) + 1
            outpoint -= ((wavetime - 60)/2) + 1

        with open(SESH, 'r') as file:
            this_sesh = json.load(file)

        index = 0

        if ('GOOD_CLIPS' not in this_sesh):
            this_sesh['GOOD_CLIPS'] = []

        if ('NUM_GOOD_WAVES' not in this_sesh):
            this_sesh['NUM_GOOD_WAVES'] = 0

        for wave in this_sesh['GOOD_CLIPS']:
            if wave['wavetime'] < wavetime:
                break
            index += 1

        if wavetime > 17:
            this_sesh['NUM_GOOD_WAVES'] += len(starts)


        this_sesh['GOOD_CLIPS'].insert(index,
            {'clip':(sys.argv[1][:-11]+"X"+sys.argv[1][-10:-3]+"MP4"),
            'wavetime':int(wavetime),
            'inpoint':int(inpoint),
            'outpoint':int(outpoint)
            }
        )
        with open(SESH, 'w') as file:
            json.dump(this_sesh, file, indent=4)
    return

            


def main():
    

    df = accl_df(read_json())
    times = get_timestamps(df)
    times = filter_em(times[0],times[1])
    times = join_em(times[0],times[1])
    times = buffer_em(times[0],times[1],10000) #fix max later
    add_best(times[0],times[1])     
    add_to_clips_file(times[0],times[1])

main()
