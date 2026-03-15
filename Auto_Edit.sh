SEARCH_DIR="/mnt/hero11sd/DCIM/100GOPRO"
TARGET_DATE="${1:-$(date +%Y-%m-%d)}"
NEXT_DAY=$(date -d "$TARGET_DATE + 1 day" +%Y-%m-%d)
INFILE="./data/lrv_list.txt"
VIDEO_NAME="./to_upload/$TARGET_DATE.MP4"
CLIPS="./data/clips.txt"
SESH="./data/this_sesh.json"

#Make list of LowResVideos (LRVs) from target day
echo "Searching in: $SEARCH_DIR for date: $TARGET_DATE"
find "$SEARCH_DIR" -type f -name "*.LRV" -newermt "$TARGET_DATE" ! -newermt "$NEXT_DAY" > $INFILE
echo "Done. Results saved to $INFILE."

#Clear clips.txt and reset this_sesh.json
> $CLIPS
jq -n '{}'> $SESH

#Get Session Start Time & Duration
START_TIME=$(date -d "$(stat -c %w $(head -n 1 "$INFILE"))" +%H:%M:%S)
END_TIME=$(date -d "$(stat -c %w $(tail -n 1 "$INFILE"))" +%H:%M:%S)
DURATION=$(($(date -d "$END_TIME" +%s) - $(date -d "$START_TIME" +%s)))
HOURS=$(date -u -d "@$(($(date -d "$END_TIME" +%s) - $(date -d "$START_TIME" +%s)))" +%H)
MINUTES=$(date -u -d "@$(($(date -d "$END_TIME" +%s) - $(date -d "$START_TIME" +%s)))" +%M)
echo "Session Started at:   $START_TIME"
#echo "Session Ended at:     $END_TIME"
#echo "Duration:             $DURATION seconds"
echo "Duration:             $HOURS HRS, $MINUTES MIN"
jq --arg st "$START_TIME" '.TIME = $st' $SESH > tmp.json && mv tmp.json $SESH
jq --arg dur "$DURATION" '.DURATION = $dur' $SESH > tmp.json && mv tmp.json $SESH
jq --arg hrs "$HOURS" '.HOURS = $hrs' $SESH > tmp.json && mv tmp.json $SESH
jq --arg min "$MINUTES" '.MINUTES = $min' $SESH > tmp.json && mv tmp.json $SESH

echo "Scanning $(wc -l < "$INFILE") Clips..."

#For Every LRV, save gpmf as JSON & write Timestamps to clips.txt
while IFS= read -r LINE; do
    node my-gpmf.js $LINE
    python3 getter.py $LINE
done < "$INFILE"

#Create Instagram Content (1080x1080 mp4s and jpgs)
./make_instagram_content.sh

#Make Instagram Post
./instagram/upload_to_instagram.sh

#Copy clips into a VOD
ffmpeg -f concat -safe 0 -i $CLIPS -c copy "./youtube/$VIDEO_NAME"

#Upload VOD to YouTube
./youtube/upload_to_youtube.sh "$VIDEO_NAME"
