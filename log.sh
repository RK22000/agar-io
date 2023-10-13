#!/bin/bash


logFile="DevLog.md"

truncate --size 0 newlog.md
echo "# $(date)" >> newlog.md
vim newlog.md
echo "---" >> newlog.md
echo "> endlog - $(date)" >> newlog.md
echo "" >> newlog.md
echo -n "#" >> newlog.md
if [[ -e "$logFile" ]]; then
	cat "$logFile" >> newlog.md
	rm "$logFile"
fi
mv newlog.md "$logFile"
