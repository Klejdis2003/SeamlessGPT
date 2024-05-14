# SeamlessGPT

## Acronyms
- **GPT**: Refers to GPT-3.5 model from Azure OpenAI.

A simple app that utilizes the Clipboard to send text to the GPT and 
pastes the response back to the Clipboard.
It is a nice way to quickly generate text using the GPT model,
it all happens within seconds.

## How to install from source
### Requirements
- Python 3.8 or higher 
- Pip
- Git
- Virtualenv

1. Clone the repository
2. Run 'install.sh' by typing `./install.sh` in the terminal in the 
    root directory of the project.
3. The script will create a virtual environment (if already not done), install the required 
    packages, and create a shortcut for the app.
4. At this point, the app should be installed and ready to use.

## How to use
1. Copy the text you want to send to the GPT model.
2. Press `Ctrl + Shift + F` to send the text to the GPT model.
3. Wait for the response (time varies). The screen briefly flashes 
    when the response is ready and the script is done.
4. Paste the response back to the desired location.

## Limitations
Since the app needs the shortcut to run, it currently only works in
Ubuntu, as the shell script is written for the shortcut system that
Ubuntu uses.