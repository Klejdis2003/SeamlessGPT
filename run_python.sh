file_parent_dir=$(dirname "$0")

# Run the python script
echo "Running python script"
source "$file_parent_dir"/.venv/bin/activate
bash -c "python $file_parent_dir/main.py; exec bash"
