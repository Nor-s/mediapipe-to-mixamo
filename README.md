# **mediapipe-to-mixamo**

-   mediapipe to mixamo
    -   landmark name => bone name
    -   mediapipe pose => mixamo skeleton structure

## 05/03

-   mediapipe to mixamo model
    -   Hips => AVG(left hip, right hip)
    -   Spine2 => AVG(Hips, Neck)
    -   Spine1 => AVG(Spine2, Hips)
    -   Spine3 => AVG(Spine2, Neck)
    -   Neck => AVG(left_shoulder, right_shoulder)
    -   Head => AVG(left_ear, right_ear)


mediapipe situp |mediapipe dance |mediapipe attack |mediapipe T pose
-|-|-|-
![](https://github.com/Nor-s/mediapipe-pose-to-json/blob/dd9e031492e9ea3c6cb4b19ce9e7552a63d85157/screenshot/mixamo_situp.gif_json_mp_.gif?raw=true) |![](https://github.com/Nor-s/mediapipe-pose-to-json/blob/dd9e031492e9ea3c6cb4b19ce9e7552a63d85157/screenshot/mixamo_dance.gif_json_mp_.gif?raw=true) |![](https://github.com/Nor-s/mediapipe-pose-to-json/blob/dd9e031492e9ea3c6cb4b19ce9e7552a63d85157/screenshot/mixamo_attack.gif_json_.gif?raw=true) |![](https://github.com/Nor-s/mediapipe-pose-to-json/blob/dd9e031492e9ea3c6cb4b19ce9e7552a63d85157/screenshot/mixamo_T_pose.gif_json_mp_.gif?raw=true)
**mixamo situp** | **mixamo dance** | **mixamo attack** | **mixamo T pose**
![](/screenshot/mixamo_situp.gif_json_mm_.gif) | ![](/screenshot/mixamo_dance.gif_json_mm_.gif)| ![](/screenshot/mixamo_attack.gif_json_mm_.gif) | ![](/screenshot/mixamo_T_pose.gif_json_mm_.gif)

## 5/5

- binding pose test (only Hips)
    
```python
def get_hip_transform(glmList):
    b_leftleg = glm.vec3(glm.distance(glmList[Mixamo.Hips], glmList[Mixamo.LeftLeg]), 0, 0)

    norm_b_leftleg = glm.normalize(b_leftleg)
    norm_leftleg = glm.normalize(glmList[Mixamo.LeftLeg])
    transform = glm.rotate(glm.mat4(1.0), glm.acos(glm.dot(norm_b_leftleg, norm_leftleg)) ,glm.cross(b_leftleg, leftleg_v))
    return glm.inverse(transform)
```

before| after
-|-
![](/screenshot/before_hip_to_binding_pose.gif)|![](/screenshot/after_hip_to_binding_pose.gif)