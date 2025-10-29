#!/bin/bash

CONFIG="./config/schedule.yml"
INTERVAL=300 # 5 minutes

# Detect OS for Chromium
if [[ "$OSTYPE" == "darwin"* ]]; then
  CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else
  CHROME="chromium-browser"
  # Hide cursor on Pi
  unclutter -idle 0 &
fi

while true; do
  NOW=$(date +"%H:%M")

  # Find current period
  CURRENT_PERIOD=$(yq e ".schedule[] | select(.start <= \"$NOW\" and .end > \"$NOW\") | .name" $CONFIG)

  # Manage periods past midnight
  if [ -z "$CURRENT_PERIOD" ]; then
    CURRENT_PERIOD=$(yq e ".schedule[] | select(.start > .end and (.start <= \"$NOW\" or .end > \"$NOW\")) | .name" $CONFIG)
  fi

  # Get URLs for current period
  URLS=($(yq e ".schedule[] | select(.name == \"$CURRENT_PERIOD\") | .urls[]" $CONFIG))

  for url in "${URLS[@]}"; do
    echo "Displaying $url [Period: $CURRENT_PERIOD]"
    
    # Launch Chromium in kiosk / fullscreen on URL
    "$CHROME" --kiosk --start-fullscreen --noerrdialogs --disable-notifications --disable-infobars "$url" &
    
    sleep $INTERVAL
  done
done
