# **MP2MM v0.0.3**

-   mediapipe to mixamo

![](./screenshot/cap.png)

-   result (on pixel3D)

![](./screenshot/animation_2.gif)

## v0.0.2 => v0.0.3 update

-   accuracy, calculation speed improvement
-   Show how the mediapipe performs pose estimation.
-   Show result the mediapipe to mixamo (plot)
-   add slider for min detection confidence
-   add checkbox for show result (Checking this will slow it down.)

## feature

-   mediapipe to mixamo animation data

-   root motion on/off (move hip)

## todo

-   hand, foot: accuracy improvement

-   webcam => pixel3D

-   fbx export (maybe pixel3D feature)

## input

-   model binding pose data

    -   sample_input_data/zom_model.json: [pixel3d](https://github.com/Nor-s/Pixel3D)->debug->model to json

-   animation gif file
    -   sample_input_data/figure.gif [link](https://news.yahoo.com/gif-guide-figure-skaters-39-jumps-olympics-171900531.html)

## references

https://medium.com/@junyingw/how-to-use-mocap-data-to-animate-your-own-avatars-in-maya-889550138365

https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2018/ENU/Maya-CharacterAnimation/files/GUID-5DEFC6E5-033C-45D5-9A0E-224E7A35131B-htm.html
