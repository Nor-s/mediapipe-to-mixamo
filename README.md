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

![](/screenshot/mixamo_situp.gif_json_mm_.gif)

![](/screenshot/mixamo_dance.gif_json_mm_.gif)

![](/screenshot/mixamo_attack.gif_json_mm_.gif)

![](/screenshot/mixamo_T_pose.gif_json_mm_.gif)
