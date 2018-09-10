#!/usr/bin/env bash
set -e
filetype='md'
watch_folder='./md'
keyword=' - alcrea.info'
printf "Watching $(realpath "$watch_folder") and subfolders for changes in .${filetype} files...\n"
while true; do
	new_hash="$(find -L "$watch_folder" -type f -name "*.$filetype" -printf '%A@ %p\n')"
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
			xdotool key 'ctrl' 'ctrl+alt+r'
			xdotool windowactivate "$current_window"
		fi
	fi
	sleep 1
done
