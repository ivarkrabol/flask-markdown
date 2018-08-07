#!/bin/bash

filetype="md"
watch_folder="md"
keyword=" - alcrea.info"
printf "Watching ${watch_folder} and subfolders for changes in .${filetype} files...\n"

while true; do
#	files="$(find "$watch_folder" -name "*.$filetype")"
#	new_hash="$(md5sum $files)"
	new_hash="$(ls -lR --time-style=full-iso "$watch_folder" | grep -E '^'"$watch_folder"'|'"$filetype"'$')"
	hash="${hash:-$new_hash}"

	if [[ "$new_hash" != "$hash" ]]; then
		hash="$new_hash"

		printf "Detected change, refreshing\n"
		current_window="$(xdotool getwindowfocus)"
		window="$(xdotool search --onlyvisible --name "$keyword" | head -1)"

		if [ -z "$window" ]; then
			printf "No visible window to refresh\n"
		else
			xdotool windowactivate "$window"
			xdotool key 'ctrl+alt+r'
			xdotool windowactivate "$current_window"
		fi
	fi

	sleep 1
done
