# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html

# Sequence generation configurations for be_generate_sequences_crowd.py
from typing import NamedTuple

# Predefined configurations
class Config(NamedTuple):
    bodies_min: int
    bodies_max: int
    x_offset: float = 1000.0
    y_offset: float = 0.0
    z_offset: float = 0.0
    x_min: float = -100.0
    x_max: float = 100.0
    y_min: float = -100.0
    y_max: float = 100.0
    yaw_min: float = 0.0
    yaw_max: float = 0.0
    num_sequences: int = 1
    unique_subjects: bool = True
    unique_sequences: bool = True # avoid repetition of subjects and animations between sequences
    camera_hfov_deg: float = 65.470451 # 28mm lens on 36x20.25mm DSLR filmback
    camera_height: float = 170.0
    override_cameraroot_location: bool = False
    safety_zone_width: float = 1000
    use_hair: bool = False
configs = {}

# be_1: 1 person in 8m x 8m area with center at camera distance 10m
config_1_1 = Config(bodies_min=1, bodies_max=1, x_offset=1000, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=1, unique_subjects=False)
configs["be_1_1"] = config_1_1

# be_2: 2 people in 8m x 8m area with center at camera distance 10m
config_2_1 = Config(bodies_min=2, bodies_max=2, x_offset=1000, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=1, unique_subjects=False)
configs["be_2_1"] = config_2_1

# be_4: 4 people in 8m x 8m area with center at camera distance 10m
config_4_1 = Config(bodies_min=4, bodies_max=4, x_offset=1000, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=1, unique_subjects=False)
configs["be_4_1"] = config_4_1

config_4_95 = Config(bodies_min=4, bodies_max=4, x_offset=1000, x_min=-300, x_max=300, y_min=-300, y_max=300, yaw_min=0, yaw_max=360, num_sequences=95, unique_subjects=True)
configs["be_4_95"] = config_4_95

# be_5: 5 people in 4m x 4m area with center at camera distance 5m
config_5_10 = Config(bodies_min=5, bodies_max=5, x_offset=500, x_min=-200, x_max=200, y_min=-200, y_max=200, yaw_min=0, yaw_max=360, num_sequences=10, unique_subjects=True)
configs["be_5_10"] = config_5_10


# be_10: 10 people in 8m x 8m area with center at camera distance 10m
config_10_1 = Config(bodies_min=10, bodies_max=10, x_offset=1000, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=1, unique_subjects=False)
configs["be_10_1"] = config_10_1

config_10_10 = Config(bodies_min=10, bodies_max=10, x_offset=1000, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=10, unique_subjects=True, camera_hfov_deg=65.470451)
configs["be_10_10"] = config_10_10

# be_10_95: Use all 95 HDRI images once
config_10_95 = Config(bodies_min=10, bodies_max=10, x_offset=1000, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=95, unique_subjects=False, camera_hfov_deg=65.470451)
configs["be_10_95"] = config_10_95

# 1 person at center, 28mm lens (HFOV 65.470451)
config_1_10 = Config(bodies_min=1, bodies_max=1, x_offset=650, x_min=0, x_max=0, y_min=0, y_max=0, yaw_min=0, yaw_max=360, num_sequences=10, unique_subjects=False, camera_hfov_deg=65.470451)
configs["be_1_10"] = config_1_10

config_1_200 = Config(bodies_min=1, bodies_max=1, x_offset=650, x_min=0, x_max=0, y_min=0, y_max=0, yaw_min=0, yaw_max=360, num_sequences=200, unique_subjects=True, camera_hfov_deg=65.470451)
configs["be_1_200"] = config_1_200

# 3 people
config_3_200 = Config(bodies_min=3, bodies_max=3, x_offset=650, x_min=-50, x_max=50, y_min=-250, y_max=250, yaw_min=0, yaw_max=360, num_sequences=200, unique_subjects=True, camera_hfov_deg=65.470451)
configs["be_3_200"] = config_3_200

configs["be_3_500"] = Config(bodies_min=3, bodies_max=3, x_offset=650, x_min=-50, x_max=50, y_min=-250, y_max=250, yaw_min=0, yaw_max=360, num_sequences=500, unique_subjects=True, camera_hfov_deg=65.470451)

configs["be_3_1000"] = Config(bodies_min=3, bodies_max=3, x_offset=650, x_min=-50, x_max=50, y_min=-250, y_max=250, yaw_min=0, yaw_max=360, num_sequences=1000, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0)
configs["be_3_1000_65"] = Config(bodies_min=3, bodies_max=3, x_offset=350, x_min=-50, x_max=50, y_min=-150, y_max=150, yaw_min=0, yaw_max=360, num_sequences=1000, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)
configs["be_3_250_65"] = Config(bodies_min=3, bodies_max=3, x_offset=500, x_min=-50, x_max=50, y_min=-150, y_max=150, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)

# 50mm lens
configs["be_3-8_250_40"] = Config(bodies_min=3, bodies_max=8, x_offset=650, x_min=-250, x_max=250, y_min=-200, y_max=200, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=39.597752)

# 1 person
configs["be_1_500"] = Config(bodies_min=1, bodies_max=1, x_offset=650, x_min=-50, x_max=50, y_min=-250, y_max=250, yaw_min=0, yaw_max=360, num_sequences=500, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)
configs["be_1_100"] = Config(bodies_min=1, bodies_max=1, x_offset=650, x_min=-50, x_max=50, y_min=-150, y_max=150, yaw_min=0, yaw_max=360, num_sequences=100, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0)

# Sports Stadium
configs["be_sport_10_5"] = Config(bodies_min=10, bodies_max=10, x_offset=0, z_offset=263.75, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=5, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0)
configs["be_sport_10_500"] = Config(bodies_min=10, bodies_max=10, x_offset=0, z_offset=263.75, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=500, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0)
configs["be_sport_3-8_250"] = Config(bodies_min=3, bodies_max=8, x_offset=0, z_offset=263.75, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0)

# High School Basketball Gym
configs["be_10_500"] = Config(bodies_min=10, bodies_max=10, x_offset=0, z_offset=0, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=500, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0)
configs["be_3-10_500"] = Config(bodies_min=3, bodies_max=10, x_offset=0, z_offset=0, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=500, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0)
configs["be_3-8_250"] = Config(bodies_min=3, bodies_max=8, x_offset=0, z_offset=0, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0)
configs["be_gym_15_100_hair"] = Config(use_hair=True, bodies_min=15, bodies_max=15, x_offset=0.0, y_offset=0.0, z_offset=0.0, x_min=-300, x_max=300, y_min=-300, y_max=300, yaw_min=0, yaw_max=360, num_sequences=100, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0, override_cameraroot_location=False)
configs["be_gym_3-10_100_hair"] = Config(use_hair=True, bodies_min=3, bodies_max=10, x_offset=0, z_offset=0, x_min=-400, x_max=400, y_min=-400, y_max=400, yaw_min=0, yaw_max=360, num_sequences=100, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0)
configs["be_gym_a_closeup_1_500"] = Config(bodies_min=1, bodies_max=1, x_offset=900, y_offset=-300, z_offset=0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=500, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451, override_cameraroot_location=True)

# Closeup
configs["be_closeup_1_500"] = Config(bodies_min=1, bodies_max=1, x_offset=0, z_offset=0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=500, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)
configs["be_closeup_1_1000"] = Config(bodies_min=1, bodies_max=1, x_offset=0, z_offset=0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=1000, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)
configs["be_closeup_1_50_hair"] = Config(use_hair=True, bodies_min=1, bodies_max=1, x_offset=0, z_offset=0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=50, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)

# ArchVizUI3
configs["be_archvizui3_3_100"] = Config(bodies_min=3, bodies_max=3, x_offset=250.0, y_offset=250.0, z_offset=0, x_min=-100, x_max=100, y_min=-100, y_max=100, yaw_min=0, yaw_max=360, num_sequences=100, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)
configs["be_archvizui3_3_250"] = Config(safety_zone_width=280.0, bodies_min=3, bodies_max=3, x_offset=250.0, y_offset=250.0, z_offset=0, x_min=-140, x_max=140, y_min=-140, y_max=140, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)

# BigOffice
configs["be_bigoffice_3_100"] = Config(bodies_min=3, bodies_max=3, x_offset=200.0, y_offset=-1000.0, z_offset=1.0, x_min=-100, x_max=100, y_min=-100, y_max=100, yaw_min=0, yaw_max=360, num_sequences=100, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)
configs["be_bigoffice_3_250"] = Config(safety_zone_width=500.0, bodies_min=3, bodies_max=3, x_offset=200.0, y_offset=-1000.0, z_offset=1.0, x_min=-150, x_max=150, y_min=-150, y_max=150, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)
configs["be_bigoffice_3_250_hair"] = Config(use_hair=True, safety_zone_width=500.0, bodies_min=3, bodies_max=3, x_offset=200.0, y_offset=-1000.0, z_offset=1.0, x_min=-150, x_max=150, y_min=-150, y_max=150, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)

# Closeup
configs["be_bigoffice_closeup_1_1000"] = Config(bodies_min=1, bodies_max=1, x_offset=200, y_offset=-1000.0, z_offset=1.0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=1000, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451)

# Suburb
# Living room, closeup
configs["be_suburb_a_closeup_1_250"] = Config(bodies_min=1, bodies_max=1, x_offset=3350.0, y_offset=-1000.0, z_offset=70.0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451, override_cameraroot_location=True)
# Kitchen, closeup
configs["be_suburb_b_closeup_1_250"] = Config(bodies_min=1, bodies_max=1, x_offset=3350.0, y_offset=1050.0, z_offset=70.0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451, override_cameraroot_location=True)
# Bedroom, closeup
configs["be_suburb_c_closeup_1_250"] = Config(bodies_min=1, bodies_max=1, x_offset=3300.0, y_offset=1200.0, z_offset=370.0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451, override_cameraroot_location=True)
configs["be_suburb_c_closeup_1_250_hair"] = Config(use_hair=True, bodies_min=1, bodies_max=1, x_offset=3300.0, y_offset=1200.0, z_offset=370.0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451, override_cameraroot_location=True)
# Outdoors, closeup
configs["be_suburb_d_closeup_1_250"] = Config(bodies_min=1, bodies_max=1, x_offset=-1200.0, y_offset=-250.0, z_offset=0.0, x_min=-10, x_max=10, y_min=-10, y_max=10, yaw_min=0, yaw_max=360, num_sequences=250, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451, override_cameraroot_location=True)
# Outdoors
configs["be_suburb_d_3-10_500"] = Config(bodies_min=3, bodies_max=10, x_offset=-1200.0, y_offset=-250.0, z_offset=0.0, x_min=-300, x_max=300, y_min=-300, y_max=300, yaw_min=0, yaw_max=360, num_sequences=500, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451, override_cameraroot_location=True)
configs["be_suburb_d_3-8_1000"] = Config(bodies_min=3, bodies_max=8, x_offset=-1200.0, y_offset=-250.0, z_offset=0.0, x_min=-300, x_max=300, y_min=-300, y_max=300, yaw_min=0, yaw_max=360, num_sequences=1000, unique_subjects=True, unique_sequences=True, camera_hfov_deg=52.0, override_cameraroot_location=True)
configs["be_suburb_d_3-8_50_hair"] = Config(use_hair=True, bodies_min=3, bodies_max=8, x_offset=-1200.0, y_offset=-250.0, z_offset=0.0, x_min=-300, x_max=300, y_min=-300, y_max=300, yaw_min=0, yaw_max=360, num_sequences=50, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451, override_cameraroot_location=True)
configs["be_suburb_d_10_100_hair"] = Config(use_hair=True, bodies_min=10, bodies_max=10, x_offset=-1200.0, y_offset=-250.0, z_offset=0.0, x_min=-300, x_max=300, y_min=-300, y_max=300, yaw_min=0, yaw_max=360, num_sequences=100, unique_subjects=True, unique_sequences=True, camera_hfov_deg=65.470451, override_cameraroot_location=True)
