# Installs all required python libraries
# Run with: 'sh install.sh'

#install python
if [ -x "$(command -v python)" ]; then
    echo "python already installed"
else
    sudo apt-get install python
fi

#install python3 just in case
if [ -x "$(command -v python3)" ]; then
    echo "python3 already installed"
else
    sudo apt-get install python3
fi

#install chromium
if [ -x "$(command -v chromium)" ]; then
    echo "chromium already installed"
else
    sudo apt-get install chromium
fi

#install Graphviz
if [ -x "$(command -v dot)" ]; then
    echo "graphviz already installed"
else
    sudo apt install graphviz
fi

pip install -U -r requirements.txt
pip3 install -U -r requirements.txt

playwright install
