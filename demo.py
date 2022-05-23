import mediapipe_helper as mph
import mixamo_helper as mmh
import json
import pyglm_helper as glmh
from multiprocessing import freeze_support
import argparse

# pyi-makespec -w -F  demo.py
# pyinstaller demo.spec
if __name__ == '__main__':
    freeze_support()
    parser = argparse.ArgumentParser(description= 'Mediapipe To Mixamo')
    parser.add_argument('arg1', help = 'model binding pose json data (pixel3d: Export model)')
    parser.add_argument('arg2', help = 'animation gif path')
    parser.add_argument('arg3', help = 'output path')
    parser.add_argument('-c', '--model_complexity', default = 1, type = int, choices=[0, 1, 2])
    parser.add_argument('-v', '--min_visibility', default = 0.5, type = float)
    parser.add_argument('-f', '--max_frame_num', default = 5000, type = int)
    parser.add_argument('--hips_move', action = 'store_true')
    args = parser.parse_args()

    model_path  =  args.arg1   
    gif_path    =  args.arg2  
    output_path =  args.arg3 
    model_complexity = args.model_complexity
    min_visibility = args.min_visibility
    max_frame_num = args.max_frame_num
    is_hips_move = args.hips_move
    try:
        mediapipe_json_object = mph.gif_to_mediapipe_json(fileName=gif_path, maxFrameNum=max_frame_num, modelComplexity= model_complexity)
        mixamo_json_object = mmh.mediapipeToMixamo(mph.get_name_idx_map(), mediapipe_json_object)
        anim_json = glmh.get_anim_json3(mixamo_json_object, model_path, is_hips_move= is_hips_move, min_visibility= min_visibility)
        with open(output_path, 'w') as f:
            json.dump(anim_json, f, indent= 2)
    except Exception as e:
        print(e)