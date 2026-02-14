#!/bin/bash
set -e

# Deployment script for Joyful Hearing website to Hostinger
# Usage: ./deploy.sh

echo "🚀 Deploying to Hostinger..."

# FTP credentials (update if needed)
FTP_HOST="147.93.17.69"
FTP_USER="u493575984"
FTP_PORT="21"

# Prompt for password securely
echo -n "Enter FTP password: "
read -s FTP_PASS
echo ""

# Use lftp for reliable FTP deployment
lftp -c "
set ftp:ssl-allow no
set net:timeout 10
set net:max-retries 2
set net:reconnect-interval-base 5
open -u $FTP_USER,$FTP_PASS $FTP_HOST
mirror --reverse --delete --verbose \
  --exclude .git/ \
  --exclude .github/ \
  --exclude .gitignore \
  --exclude node_modules/ \
  --exclude .DS_Store \
  --exclude deploy.sh \
  --exclude README.md \
  ./ ./
bye
"

echo "✅ Deployment complete!"
echo "Visit: https://joyfulhearingandspeech.com"
