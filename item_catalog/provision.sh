#!/usr/bin/env bash
# Provisioning script for Item Catalog

# Installation Settings
PROJECT_NAME=$1
MOTD=$2

VIRTUALENV_NAME=$PROJECT_NAME
HOME=/home/vagrant
PROJECT_DIR=$HOME/$PROJECT_NAME
VIRTUALENV_DIR=$HOME/.virtualenvs/$PROJECT_NAME

#Make sure it will reload VMWare tools if the Kernel is upgraded
echo "answer AUTO_KMODS_ENABLED yes" | sudo tee -a /etc/vmware-tools/locations

# Enable EPEL Repo
yum -y install epel-release

# Install updates
yum -y update

#Install the components we need
yum -y install python-pip

# virtualenv global setup
if [[ ! -f /usr/local/bin/virtualenv ]]; then
    pip install virtualenv virtualenvwrapper stevedore virtualenv-clone
fi

# virtualenv setup for project
su - vagrant -c "/usr/bin/virtualenv $VIRTUALENV_DIR && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    $VIRTUALENV_DIR/bin/pip install -r $PROJECT_DIR/requirements.txt"

echo "source /usr/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
echo "workon $VIRTUALENV_NAME" >> /home/vagrant/.bashrc

# Setup MOTD
echo -e $MOTD > /etc/motd
