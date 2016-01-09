# Item Catalog
## Purpose
Completed as part of Project 3 for the Udacity Full Stack Nonodegree.

## Requirements
1.  [Vagrant](https://www.vagrantup.com/)
1.  [VirtualBox](https://www.virtualbox.org/) or [VMware Fusion/Workstation](https://www.vmware.com/)

## Usage
1.  Clone repository: ```git clone https://github.com/wduncanfraser/item_catalog.git```.
1.  Run ```vagrant up``` and then ```vagrant ssh``` to provision and log into the vm.
1.  Once logged into the VM, you should already be in the project directory. If not, navigate to the project files with ```cd /home/vagrant/item_catalog```.
1.  Run ```python item_catalog.py``` to run the flask application for the item catalog.
1.  Open a web browser and navigate to ```http://localhost:5000```.

## Structure
+   itemcatalog/: Item Catalog Flask App directory
    +   Vagrantfile: Vagrant VM configuration.
    +   provision.sh: Provisioning script for the Vagrant VM. Installs the desired packages and configures the flask application.

## External Resources
1. SQLAlchemy
1. Flask
1. Flask-SQLAlchemy

## Legal
Author: [W. Duncan Fraser](duncan@wduncanfraser.com)

License: [MIT License](LICENSE)