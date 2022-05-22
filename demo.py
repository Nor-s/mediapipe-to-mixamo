import mediapipe_helper as mph
import mixamo_helper as mmh
import json
import pyglm_helper as glmh
from multiprocessing import freeze_support
import sys

if __name__ == '__main__':
    freeze_support()
    argument = sys.argv
    del argument[0]
    model_path  =  argument[1]   
    gif_path    =  argument[2]   
    output_path =  argument[3]  
    try:
        mediapipe_json_object = mph.gif_to_mediapipe_json(fileName=gif_path, maxFrameNum=5000, modelComplexity=1)
        mixamo_json_object = mmh.mediapipeToMixamo(mph.get_name_idx_map(), mediapipe_json_object)
        anim_json = glmh.get_anim_json3(mixamo_json_object, model_path, is_hips_move= True, min_visibility= 0.6)
        with open(output_path, 'w') as f:
            json.dump(anim_json, f, indent= 2)
    except Exception as e:
        print(e)
    

