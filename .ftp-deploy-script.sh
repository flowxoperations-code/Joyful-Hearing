#!/bin/bash
# Manual FTP upload script to test deployment

echo "Uploading index.html and mohini-profile.jpg to test FTP..."

lftp -u u493575984 ftp://147.93.17.69 <<EOF
cd public_html
put index.html
cd assets
put assets/mohini-profile.jpg
bye
EOF

echo "Upload complete!"
