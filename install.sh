# Installs all required python libraries
# Run with: 'sh install.sh'

INT3="3"

#install python
if [ -x "$(command -v python)" ]; then

    # python VERsion
    PYV="$(python --version 2>&1 | grep -Po '(?<=Python )(.)')"

    # if python 2 installed
    if [ $PYV==$INT3 ]; then
        
        echo "python2 already installed"
        
        # check for python3 install
        if [ -x "$(command -v python3)" ]; then
            echo "python3 already installed"
        else
            apt install python3
        fi

        VER=$INT3

    fi

else # python is not installed
    apt install python
fi

if [ $VER==$INT3 ]; then

    # install the things with python3
    echo "installing python3 requirements"

else 

    # install the things with python
    echo "installing python requirements"

fi

# other things

apt update

# install nginx
apt install nginx

# npm
if [ -x "$(command -v npm)" ]; then
    echo "npm already installed"
else
    apt install npm
fi

cd course-utility
npm install
