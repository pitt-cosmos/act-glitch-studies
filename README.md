# ACT Glitch Studies
ACT Glitch studies to characterize all glitches and find FRBs hopefully!

## Overview
There are three major components in the analysis code that are applied in a more-or-less consecutive order.

#### 1. Compile glitch cuts
Taking the existing glitch finder written by Loic, we first compile all the glitch cuts from a list of TODs, and save the results.
The codes for this step are stored in the folder `compile_glitch_cuts`. The outputs are saved in the output folder.

#### 2. Find coincident signals
Coincident signals (sometimes called "cosig" in codes) refer to glitches that occur in both frequencies (90GHz and 150GHz) in a given pixel. 

- A **strict** version refers to when both polarization channels for each frequency are glitching. 
- A **loose** version refers to any polarization channels see the glitch. 

(note that only TES detectors are considered) 

The coincident signals found in all pixels for each TOD are compiled based on the output from Step 1, and saved. 

In addition, we also overlay coincident signals in a temporal order to identify what we called **physical events** that are temporally correlated glitches affecting multiple 
detectors in multiple pixels. These events are also returned.

The exported data consists of a dictionary with two keys 

- `"coincident_signals"` which contains coincident signals in each pixel
- `"peaks"` which contains physical events with each entry containing four numbers: `[t_start, t_end, duration, n_pixels]`

This data is exported for each TOD and serves as the starting point for physics studies. 

A recently compiled outputs for this step is located at (on feynman cluster)

```
/mnt/act3/users/yilun/act-glitch-studies/outputs/coincident_signals_subset
```


#### 3. Study of events (EventLoop)
An analysis framework called **EventLoop** is developed to facilitate the study of events (temporally correlated coincident signals). 

It serves as a pipeline of different routines that can be applied to the data. Routines can be event filters, data saving, plotting etc. See `get_tracks/get_tracks.py` for an example usage. 


## Instructions
1. Add the project folder to your pythonpath.

## Development Guidelines
1. Class name use camel case like `GetTrackWithSpread`. 
2. Method name use lowercase with underscores like `get_tod_id`. 
3. Path always include `/` at the end. 
4. Always run scripts in project root directory, like `python get_tracks/get_tracks.py`
5. Organize independent codes into its subfolder instead of project root directory
6. Script `slurm_submit.py` assumes your script has `sys.argv[1]` to be starting index, `sys.argv[2]` to be ending index
7. Inline comment starts after two spaces
8. Class attributes use lowercase with underscores, starting with underscore like `_tod_id`
9. Develop new features in new branches, and submit merge requests when tested working. 
