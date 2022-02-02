# Installs all required python libraries
# Run with: 'sh install.sh'

pip install -r requirements.txt

#install chromium
if ! command -v chromium &>/dev/null 
then
    sudo apt-get install chromium
fi

#install Graphviz
if ! command -v graphviz &>/dev/null 
then
    sudo apt install graphviz
fi