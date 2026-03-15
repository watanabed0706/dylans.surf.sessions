
# Path Variables Session data
SESH="./data/this_sesh.json"
THM="./instagram/to_upload/0_thumbnail.jpg"
TMP="temp.jpg"
SD_CARD="/mnt/hero11sd/DCIM/100GOPRO/"
VIDPATH="$(jq -r '.GOOD_CLIPS[0].clip' $SESH)"
#There's a YEAR_JSON Path Defined at bottom too

# Data Regarding Session Date
DATE=$(date -d "$(stat -c %w $VIDPATH)" +%Y-%m-%d)
NEXT_DATE=$(date -d "$DATE + 1 day" +%Y-%m-%d)
WKDAY=$(date -d $DATE +%A)
YEAR=$(date -d $DATE +%Y)
MONTH=$(date -d $DATE +%B)
DAY=$((("$(date -d $DATE +%d)") - 1))

# Data Regarding Session Duration
DURATION=$(echo "scale=2; $(jq -r '.DURATION' $SESH) / 3600" | bc)
HOURS=$(jq -r '.HOURS' $SESH)
MINUTES=$(jq -r '.MINUTES' $SESH)

# Number of Waves (over 17seconds)
NUM_WAVES=$(jq -r '.NUM_GOOD_WAVES' $SESH)

# Picking a Thumbnail (2/3rds into Best Wave OR Sesh's most recent JPG)
FRAME=$(echo "scale=2; $(jq -r '.GOOD_CLIPS[0].inpoint' $SESH) + ($(jq -r '.GOOD_CLIPS[0].wavetime' $SESH) * 0.67)" | bc)
JPG=$(find $SD_CARD -name "*.JPG" -newermt $DATE ! -newermt $NEXT_DATE -printf "%T+ %p\n" | sort -r | head -1 | cut -d' ' -f2-)
if [ -z "$JPG" ]; then
    ffmpeg -loglevel error -y -ss $FRAME -i $VIDPATH -frames:v 1 $THM
else
    cp $JPG $THM
fi

# Data Regarding Session Start time (parsed to AM/PM)
# Reason: Passing ffmpeg a Str containing ':' is BAD News
START_TIME="$(jq -r '.TIME' $SESH)"
START_HR="$(date -d $START_TIME +%l)"
START_MIN="$(date -d $START_TIME +%M)"
AM_PM="$(date -d $START_TIME +%p)"

# ffmpeg flags
QUIET='-loglevel error -y'
FONT='drawtext=moonlit_flow/MoonlitFlow-Regular.ttf:fontcolor=white'
BORD='bordercolor=black:borderw'
LINEAR="-vf lenscorrection=k1=-0.225:k2=0.03"
CROP="-vf crop=min(iw,ih):min(iw,ih)"
SCALE="-vf scale=1080:1080"
CROP1080="-vf crop=ih:ih,scale=1080:1080"


#Make Horizon look More Linear
# & less fisheye like
ffmpeg $QUIET -i $THM $LINEAR $TMP
mv $TMP $THM

#CROP it to Size
ffmpeg $QUIET -i $THM $SCALE $TMP
mv $TMP $THM

# Function for Text Overlays
add_text(){ # text, size, right%, down%
    ffmpeg $QUIET -i $THM -vf "$FONT:$BORD=5:text=$1:fontsize=$2:x=(w-text_w)*$3:y=(h-text_h)*$4" $TMP
    mv $TMP $THM
}

# Function for Making Square Clip (1080p 30fps H264 8Mbps)
make_clip() { #input , inpoint , outpoint , output
    ffmpeg $QUIET -i "$1" -ss $2 -to $3 $LINEAR $SCALE -r 30 -c:v libx264 -b:v 8M "./instagram/to_upload/$4.mp4"
}


# TEXT OVERLAYS!! & Lots of 'Em
add_text $(date -d $DATE +%b) 180 0.05 0.05 #MONTH (3-char)
add_text $(date -d $DATE +%Y) 90 0.08 0.2   #YEAR
add_text $(date -d $DATE +%d) 300 0.4 0.05  #DAY of month
add_text $(date -d $DATE +%A) 100 0.05 0.35 #DAY of Week
add_text "______" 200 0.06 0.28
add_text "$START_HR'\:'$START_MIN $AM_PM" 60 0.05 0.42
add_text "$NUM_WAVES" 100 0.8 0.95
add_text "GOOD" 45 0.93 0.91                
add_text "WAVES" 45 0.95 0.95
add_text "HOURS" 45 0.95 0.85
add_text "$HOURS'\:'$MINUTES" 100 0.8 0.85


# Make Square Clips of the 3 best waves
count=0
jq -c '.GOOD_CLIPS[]' "$SESH" | while read -r wave; do
    ((count++))

    if [ "$count" -gt 3 ]; then
        break
    fi

    clip=$(echo "$wave" | jq -r '.clip')
    inpoint=$(echo "$wave" | jq -r '.inpoint')
    outpoint=$(echo "$wave" | jq -r '.outpoint')

    echo "Editing Wave $count"
    make_clip $clip $inpoint $outpoint "${count}_wave" < /dev/null
    echo "Done w/ Wave $count!"
    
done

# Make a year_json, if there isn't one
YEAR_JSON="./data/$YEAR.json"
if [ ! -s "$YEAR_JSON" ]; then
    python3 make_year_json.py $YEAR $YEAR_JSON
fi
jq --arg month "$MONTH" --argjson day "$DAY" --argjson duration "$DURATION" '.[$month][$day] = $duration' "$YEAR_JSON" > tmp.json && mv tmp.json "$YEAR_JSON"

#make month & year graphs
python3 make_graphs.py $DATE

