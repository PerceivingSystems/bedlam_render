# Unreal Editor BEDLAM Asset Filesystem Hierarchy

## BEDLAM Core
```
UE_5.0/Engine/Content/PS/Bedlam/Core/
├── BE_CineCameraActor_Blueprint.uasset
├── BE_GroundTruthLogger.uasset
├── EditorScripting
│   └── BEDLAM.uasset
├── LICENSE.md
├── Materials
│   ├── BE_ClothingOverlayActor.uasset
│   ├── LightProbe
│   │   ├── BE_LightProbe.uasset
│   │   ├── BE_LightProbe_Black.uasset
│   │   ├── BE_LightProbe_Chrome.uasset
│   │   ├── BE_LightProbe_Gray.uasset
│   │   ├── BE_LightProbe_White.uasset
│   │   ├── BE_Skin1.uasset
│   │   └── BE_Skin6.uasset
│   ├── M_Clothing.uasset
│   ├── M_SMPLX.uasset
│   ├── M_SMPLX_Clothing.uasset
│   ├── M_SMPLX_Hidden.uasset
│   ├── M_SMPLX_White.uasset
│   └── Textures
│       ├── Meshcapade_CC_BY-NC_4_0
│       │   ├── SMPLX_eye.uasset
│       │   └── skin_m_white_01_ALB.uasset
│       ├── T_rp_aaron_posed_002_texture_01_diffuse.uasset
│       ├── T_rp_aaron_posed_002_texture_01_normal.uasset
│       └── rp_aaron_posed_002_texture_01.uasset
└── Python
    ├── create_level_sequences_csv.py
    ├── create_movie_render_queue.py
    └── render_movie_render_queue.py
```

## SMPL-X Animated Bodies
```
UE_5.0/Engine/Content/PS/Bedlam/SMPLX
├── female_30_it_4031
│   ├── female_30_it_4031_0000.uasset
│   ├── ...
│   └── female_30_it_4031_0024.uasset
├── ...
└── rp_jessica_posed_009
    ├── rp_jessica_posed_009_1001.uasset
    ├── ...
    └── rp_jessica_posed_009_1099.uasset
```

## Body Materials/Textures
```
UE_5.0\Engine\Content\PS\Meshcapade
└── SMPL
    ├── MC_texture_skintones
    │   ├── female
    │   │   └── skin
    │   │       ├── skin_f_african_01_ALB.uasset
    │   │       ├── ...
    │   │       └── skin_f_white_07_ALB.uasset
    │   └── male
    │       └── skin
    │           ├── skin_m_african_01_ALB.uasset
    │           ├── ...
    │           └── skin_m_white_07_ALB.uasset
    └── Materials
        ├── MI_skin_f_african_01_ALB.uasset
        ├── ...
        └── MI_skin_m_white_07_ALB.uasset
```

## Clothing Simulation/Materials/Textures
```
UE_5.0/Engine/Content/PS/Bedlam/Clothing/
├── Materials
│   ├── rp_aaron_posed_002
│   │   ├── MI_rp_aaron_posed_002_texture_01.uasset
│   │   ├── MI_...
│   │   ├── MI_rp_aaron_posed_002_texture_17.uasset
│   │   ├── T_rp_aaron_posed_002_texture_01_diffuse.uasset
│   │   ├── T_rp_aaron_posed_002_texture_01_normal.uasset
│   │   ├── ...
│   │   ├── T_rp_aaron_posed_002_texture_17_diffuse.uasset
│   │   └── T_rp_aaron_posed_002_texture_17_normal.uasset
│   ├── ...
│   └── rp_jessica_posed_009
│       ├── MI_rp_jessica_posed_009_texture_01.uasset
│       ├── ...
│       ├── MI_rp_jessica_posed_009_texture_18.uasset
│       ├── T_rp_jessica_posed_009_texture_01_diffuse.uasset
│       ├── T_rp_jessica_posed_009_texture_01_normal.uasset
│       ├── ...
│       ├── T_rp_jessica_posed_009_texture_18_diffuse.uasset
│       └── T_rp_jessica_posed_009_texture_18_normal.uasset
├── MaterialsSMPLX
│   └── Textures
│       ├── rp_aaron_posed_002_texture_01.uasset
│       ├── ...
│       └── rp_jessica_posed_009_texture_18.uasset
├── rp_aaron_posed_002
│   ├── rp_aaron_posed_002_1001_clo.uasset
│   ├── ...
│   └── rp_aaron_posed_002_1099_clo.uasset
├── ...
└── rp_jessica_posed_009
    ├── rp_jessica_posed_009_1001_clo.uasset
    ├── ...
    └── rp_jessica_posed_009_1099_clo.uasset
```

# HDRI
```
UE_5.0/Engine/Content/PS/Bedlam/HDRI/
└── 4k
    ├── abandoned_church.uasset
    ├── ...
    └── zhengyang_gate.uasset
```
