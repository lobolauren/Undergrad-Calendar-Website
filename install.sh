# Installs all required python libraries
# Run with: 'sh install.sh'

pip install -r requirements.txt

#install chromium
if ! command -v chromium >/dev/90.0.4430
then
    sudo apt-get install chromium
else
    echo "chromium already installed"
fi

#install Graphviz
if ! command -v graphviz >/dev/2.40.1 
then
    sudo apt install graphviz
else
    echo "graphciz already installed"
fi