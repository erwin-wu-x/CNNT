# CNNT: Continuous Nearest Neighbor Tracking   

**Authors:** Shaoxun Wu, Weiqing Wang, Qian wang

CNNT  is Continuous Nearest Neighbor Real-Time Microbubble Tracking Algorithm for Ultrasound Localization Microscopy, with an efficient nearest neighbor data structure for continuously tracking bubbles.  CNNT is a robust novel CPU-based real-time microbubble tracking algorithm, wihch is built by python and MATLAB file io.

### Related Publications:

Shaoxun Wu, Weiqing Wang, Qian wang CNNT: **Continuous Nearest Neighbor Real-Time Microbubble Tracking Algorithm for Ultrasound Localization Microscopy**   ShanghaiTech CS270 DIP final project. [PDF](https://github.com/erwin-wu-x/CNNT/blob/main/report.pdf). 

# Prerequisites

We have tested the library in **Ubuntu 18.04**, **20.04** and **Windows 10&11**. A powerful computer (though we aimed at efficient and real-time) will ensure real-time performance and provide more stable and accurate results.

## MATLAB

```
ToolBoxRequires = {'Communications','Bioinformatics','Image Processing','Curve Fitting','Signal Processing','Statistics and Machine Learning','Computer Vision Toolbox'};
```

## Python

```
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy scipy sklearn
```

## Python (optional)

```
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple tqdm multiprocessing cv2 matplotlib
```

# CNNT framework Example (Linux needed)

First, exacting the images (opencv, matplotlib needed) or just download [figures]().

```
cd Dataset && mkdir raw
cd raw # download raw mat files
python3 extractor.py
cd ../..
```

Now we have figs, then run Localization.m in MATLAB to get the locations.

Then we can save tracks with Save Trajectories Example.

Make sure all the trajectories are saved correctly, then run render.m in MATLAB to get the results.

# Time counter Example

(tqdm needed)

If you want to count the processing time, directly run main_time.py.

It will be like:

```
Patch 1, average bubble num: 82.245: 100%|███████████████████████████████████████████████████████▉| 799/800 [00:00<00:00, 1813.68it/s]
```

The right side item is the FPS result.

# Save Trajectories Example

(multiprocessing needed)

When you have locations, you can run the main_accelerate.py.

```
python3 code/main_accelerate.py -h
usage: main_accelerate.py [-h] [-N PROCESS_NUM] [-M METHOD] [-P PCONSTANT] [-D MAX_DISTANCE] [-S SAVE_TRACK]

Tracking bubbles.

optional arguments:
  -h, --help            show this help message and exit
  -N PROCESS_NUM, --process_num PROCESS_NUM
  -M METHOD, --method METHOD
  -P PCONSTANT, --pconstant PCONSTANT
  -D MAX_DISTANCE, --max_distance MAX_DISTANCE
  -S SAVE_TRACK, --save_track SAVE_TRACK
```
