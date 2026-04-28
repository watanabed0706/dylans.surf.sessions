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

### Auto_Edit.sh:
The Main Script in the Program

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

