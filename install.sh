file_parent_dir=$(dirname "$0")

if [ ! -d "$file_parent_dir"/.venv ]; then
    echo "Creating virtual environment"
    python3 -m venv "$file_parent_dir"/.venv
    source "$file_parent_dir"/.venv/bin/activate
    pip install -r "$file_parent_dir"/requirements.txt
fi

# check if the shortcut is already set
#if yes, prompt if the user wants to overwrite it
# if no, set the shortcut

echo "Setting shortcut to CTRL+ALT+F"
if [ -n "$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)" ]; then
    echo "CTRL+ALT+F is already being used for a different shortcut."
    read -p "Do you want to overwrite the shortcut? (y/n): " overwrite
    if [ "$overwrite" == "n" ]; then
        echo "Exiting"
        exit 0
    fi
fi

chmod +x "$file_parent_dir"/run_python.sh
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ name 'Open Clipboard Gpt Tracker'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ command "/bin/bash $file_parent_dir/run_python.sh"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ binding '<Control><Alt>F'
echo "Shortcut set to CTRL+ALT+F"