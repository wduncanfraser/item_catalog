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
1.  Run ```python run.py``` to run the flask application for the item catalog.
1.  Open a web browser and navigate to ```http://localhost:5000```.

## Structure
+   itemcatalog/: Item Catalog Flask application directory.
+   instance/: Instance specific files and configuration. Excluded from repository.
    1.  config.py: Instance specific configuration. Overrides values in root config.py.
+   config.py: Flask configuration.
+   requirements.txt: Python package requirements, installed during provisioning.
+   run.py: Python file to start development server.
+   setup.py: Python file to setup fresh application/database.
+   Vagrantfile: Vagrant VM configuration.
+   provision.sh: Provisioning script for the Vagrant VM. Installs the desired packages and configures the flask application.

## External Resources
+   Javascript/CSS Libraries
    1.  Material Design Light
    1.  Toastr
+   Python Packages
    1.  SQLAlchemy
    1.  Flask
    1.  Flask-SQLAlchemy
    1.  WTFOrms
    1.  Flask-WTF

## Legal
Author: [W. Duncan Fraser](duncan@wduncanfraser.com)

License: [MIT License](LICENSE)