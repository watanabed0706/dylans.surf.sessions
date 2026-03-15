TARGET_DIR="/home/dylan/gopro/instagram/to_upload"
PORT=8080

# Check API Keys

# Start Python HTTP Server & Open Tunnel with NGROK
cd $TARGET_DIR
python3 -m http.server $PORT > /dev/null & PYTHON_PID=$!
ngrok http $PORT > /dev/null & NGROK_PID=$!
echo "Server started (PID: $PYTHON_PID) and ngrok tunnel active (PID: $NGROK_PID)"

# Get NGROK URL to HTTP Server
echo -n "Waiting for ngrok to generate URL..."
until curl -s http://localhost:4040/api/tunnels > /dev/null; do
    sleep 1
    echo -n "."
done
echo "Ready!"
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
echo "Your public URL is: $NGROK_URL"

# Publish MP4s/JPGs in to_upload to An Instagram Carousel
# (Ordered by File Name ASCII asc)
python3 ../graphAPI/publish.py $NGROK_URL

# Kill HTTP server & NGROK Tunnel
kill $PYTHON_PID
kill $NGROK_PID
echo "Finished and cleaned up."