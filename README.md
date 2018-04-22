# ACT Glitch Studies
ACT Glitch studies to characterize all glitches and find FRBs hopefully!

## Instructions
To have the best user experience, add the project folder to your pythonpath.

## Conventions
1. Class name use camel case like `GetTrackWithSpread`. 
2. Method name use lowercase with understores like `get_tod_id`. 
3. Path always include `/` at the end. 
4. Always run scripts in project root directory, like `python get_tracks/get_tracks.py`
5. Organize independent codes into its subfolder instead of project root directory
6. Script slurm_submit.py assumes your script has `sys.argv[1]` to be starting index, `sys.argv[2]` to be ending index
