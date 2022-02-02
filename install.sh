# Installs all required python libraries
# Run with: 'sh install.sh'

pip install -r requirements.txt

#install chromium
if [ -x "$(command -V chromium)" ]; then
    echo "chromium already installed"
else
    sudo apt-get install chromium
fi

#install Graphviz
if [ -x "$(command -V dot)" ]; then
    echo "graphciz already installed"
else
    sudo apt install graphviz 
fi