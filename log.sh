#!/bin/bash


logFile=${1:-"DevLog"}
editor=${2:-"vim"}

truncate --size 0 newlog.md
echo "# $(date)" >> newlog.md
$editor newlog.md
echo "---" >> newlog.md
echo "> endlog - $(date)" >> newlog.md
echo "" >> newlog.md
echo -n "#" >> newlog.md
if [[ -e $logFile.md ]]; then
	cat $logFile.md >> newlog.md
	rm $logFile.md
fi
mv newlog.md $logFile.md