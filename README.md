# Dylan's Surf Sessions (CPSLO CS Senior Project)

As my senior Project, I decided to build a program that automatically:
* Reads through files on my GoPro's SD-Card
* Detects waves ridden via embedded GPMF Accelerometer/Gyroscope data
* Creates wave clips utilizing those timestamps
* Reports session details (date/time, sesh duration, # of Waves, ...)
* Posts the clips to Instagram/YouTube

## Usage:

* $git clone https://github.com/watanabed0706/dylans.surf.sessions
* ??
* ./Auto_Edit.sh $DATE $PATH_TO_SD_CARD

## Requirements:
### GoPro HERO 11
  - Other HERO models may work...
    - Most models (11 included) order data, {Z,X,Y}
    - HERO 6 orders as {Y,-X,Z}
    - Other critical differences may exist to...

### Computer with a Debian-Based OS
  - I used ubuntu-server 24.04.1 LTS

### USB connection to SD-Card
  - Must be mounted before running

### Buissiness Instagram Account (optional)
  - Required for Automatic Uploads

### Youtube Account (optional)
  - Required for Automatic Uploads

## Code Breakdown:

### The data directory:
- lrv_list.txt:
    - Lists all Low Resolution Videos from target date
    - Overwritten every run
- this_sesh.json:
    - Holds Info about the session details
    - (date/time, sesh duration, # of Waves, ...)
    - Overwritten every run
- clips.txt:
    - A list of Wave Timestamps
    - Formatted specifically for usage with ffmpeg
    - Overwritten every run
- YYYY.json:
    - Holds session durations for the whole year
    - Overwrites only single value at Target_Date
- gpmf.json:
    - Where my-gpmf.js saves data for getter.py to process it
    - Overwritten every clip

### Auto_Edit.sh: (The Main Script)

  - Arguments:
    - Target_Date (YYYY-MM-DD)
      - Default: Today's Date
    - SEARCH_DIR
      - Default: "/mnt/hero11sd/DCIM/100GOPRO"

  - Execution Gist:
    - Gathers Sesion Info and LRVs
    - For every LRV, my-gpmf.js and getter.py
    - ./make_instagram_content.sh
    - ./upload_to_instagram.sh
    - Makes a VOD for Youtube
    - Uploads to Youtube

### my-gpmf.js (Retrieving Metadata from the LRV files):
Despite the name of the program, the implementation is not mine...

This whole project wouldn't have been possible without [GoPro](https://github.com/gopro) releasing [GPMF](https://github.com/gopro/gpmf-parser) as Open Source and [JuanIrache](https://github.com/JuanIrache)'s [gmpf-extract](https://github.com/JuanIrache/gpmf-extract) & [gopro-telemetry](https://github.com/juanirache/gopro-telemetry)

### getter.py: (Wave Detection Logic)
Once my-gpmf.js has saves the data streams as a JSON file (gmpf.json), getter.py reads it and converts it to a pandas DataFrame for analysis. GMPF contains an extensive amount of metadata, of which only a small portion is necessary for wave detection. In getter.py, the six attributes used are...
  - X-Acceleration
  - Y-Acceleration
  - Z-Acceleration
  - X-Rotation
  - Y-Rotation
  - Z-Rotation
The sample rate for each of these data points is 200 times a second, and I've found their accuracy to be relatively high. Whenever the camera is sitting perfectly still, an acceleration of roughly 9.81m/s^2 in the upward direction and 1.2m/s^2 in the forward direction. The upward acceleration is caused by the normal force resisting gravity. As for the anomaly in forward acceleration, I have no idea what it is caused by.

The Previous Original Logic for wave detection was searching for moments of near free fall. In other words, instances when the accelerometer did not detect any major forces (gravity included) in any particular direction. It would stitch those within 4 seconds of eachother together as intervals, and later merge any close intervals together. Any intervals over 14 seconds were considered waves. Though a seemingly over-simplified and random heuristic, it worked rather consistently for most shortboarding waves.

The New Logic behind wave detection utilizes a machine learning model trained on ___ samples from 10 different sessions to find more specific patterns from waves. This also allows classification of more than just waves but also other events while surfing such as duck-dives and specific maneuvers such as cutbacks.

### 

