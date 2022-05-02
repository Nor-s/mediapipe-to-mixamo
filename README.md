# **mediapipe-to-mixamo**

- mediapipe to mixamo
    - landmark name => bone name
    - mediapipe pose => mixamo skeleton structure

## 05/03

- mediapipe to mixamo model
    - Hips => AVG(left hip, right hip)
    - Spine2 => AVG(Hips, Neck)
    - Spine1 => AVG(Spine2, Hips)
    - Spine3 => AVG(Spine2, Neck)
    - Neck => AVG(left_shoulder, right_shoulder)
    - Head => AVG(left_ear, right_ear)

![](/output/mixamo_situp.gif.json.json.gif)

![](/output/mixamo_dance.gif.json.json.gif)

![](/output/mixamo_attack.gif.json.json.gif)

![](/output/mixamo_T_pose.gif.json.json.gif)