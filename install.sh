# Installs all required python libraries
# Run with: 'sh install.sh'

#pip install -r requirements.txt

#install requirments
if [ -x "$(command -v -r requirements.txt)" ]; then
    echo -r requirements.txt+" already installed"
else
    pip install -r requirements.txt
fi

#install chromium
if [ -x "$(command -v chromium)" ]; then
    echo "chromium already installed"
else
    sudo apt-get install chromium
fi

#install Graphviz
if [ -x "$(command -v dot)" ]; then
    echo "graphciz already installed"
else
    sudo apt install graphviz 
fi