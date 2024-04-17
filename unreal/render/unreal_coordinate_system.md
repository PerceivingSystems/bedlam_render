# BEDLAM Unreal Coordinate System Information
BEDLAM uses `Unreal coordinate system` for specifying the render sequences (`be_seq.csv`) and for storing the camera ground truth intrinsic and extrinsic parameters (`ground_truth/camera/seq_XXXXXX_camera.csv`).

+ Unit: [cm]
+ `X`: forward, `Y`: right, `Z`: up
+ Default camera orientation: looking along `+X`
+ Camera rotation: specified in Tait-Bryan Euler angles
  + `First yaw around world Z-axis, then pitch around new local Y-axis, then roll around new local X-axis.`
  + Yaw rotation is `left-handed`, pitch+roll rotations are `right-handed`

## Camera ground truth .csv file details

+ Intrinsics
  + `sensor_width`, `sensor_height`: [mm]
    + All BEDLAM sequences use same camera sensor 36mm x 20.25mm
  + `focal_length`: [mm]
  + `hfov`: [deg]
    + Resulting horizontal view of sensor width + focal length combination

+ Extrinsics
  + `x`, `y`, `z`: Unreal world location in [cm]
  + `yaw`, `pitch`, `roll`: Unreal world camera rotation in [deg]
    + yaw => pitch' => roll''

### Camera extrinsics example
+ File: `20221010_3_1000_batch01hand\ground_truth\camera\seq_000000_camera.csv`
  + Image: `seq_000000_0000.png`

```
name,x,y,z,yaw,pitch,roll,focal_length,sensor_width,sensor_height,hfov
seq_000000_0000.png,5.058579,-9.743741,168.953232,1.468127,-2.905068,2.813995,36.905,36,20.25,52
...
```

1. Position camera at world location (`5.058579`,`-9.743741`,`168.953232`).
2. Camera first faces default direction (`+X`).
3. Yaw rotation: Rotate around `world` `Z` axis by `1.468127` deg (left-hand rule). Camera will rotate to the right.
4. Pitch rotation: Rotate around new `local` `Y` axis by `-2.905068` deg (right-hand rule). Camera will pitch down.
5. Roll rotation: Rotate around new `local` `X` axis by `2.813995` deg (right-hand rule). Camera will rotate clockwise.
