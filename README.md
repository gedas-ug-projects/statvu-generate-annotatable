# Statvu Access 

The purpose of this repository is to automate the process of creating video and 2D projection images side by side.

# Setup

```bash
python3 -m venv .venv
# Window
source .venv/Scripts/activate
# Linux
source .venv/bin/activate
pip install -r requirements.txt
```

# Script Templates

```bash
python -m src.scripts.GenerateForAFrame \
--vid_path "[path to video]" \
--pos_2d_path "[path to 2d track json]" \
--game_log_path "[path to game log]" \
--frame_num 3500

python -m src.scripts.GenerateForAVideo \
--vid_path "[path to video]" \
--pos_2d_path "[path to 2d track json]" \
--game_log_path "[path to game log]" \
--frame_inc 15

python -m src.scripts.GenerateForAllPeriods \
--frame_inc 15
```

use `-h` for help with the scripts

# Directory Definition

`./output/`: the default directory for all execution output

`./data/`: the default directory for all preprocessing data [legacy as dataset has been moved to sunflower]

`./src/auth/`: the default directory for storying Google Drive API credentials (legacy)

`./src/notebooks/`: contains all jupyter notebooks used by the author for debugging and sandbox environments

`./src/scripts/`: the default directory for all automation scripts 


# AWS S3 Setup
