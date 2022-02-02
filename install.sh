# Installs all required python libraries
# Run with: 'sh install.sh'

pip install -r requirements.txt

#install chromium
if ! command -v chromium >/dev/null 
then
    sudo apt-get install chromium
else
    echo "chromium already installed"
fi

#install Graphviz
if ! command -v graphviz 2>/dev/null 
then
    sudo apt install graphviz
else
    echo "graphciz already installed"
fi