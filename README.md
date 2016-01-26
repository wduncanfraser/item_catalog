# Item Catalog
## Purpose
Completed as part of Project 3 for the Udacity Full Stack Nonodegree.

## Requirements
1.  [Vagrant](https://www.vagrantup.com/)
1.  [VirtualBox](https://www.virtualbox.org/) or [VMware Fusion/Workstation](https://www.vmware.com/)

## Usage
1.  Clone repository: `git clone https://github.com/wduncanfraser/item_catalog.git`.
1.  Run `vagrant up` and then `vagrant ssh to provision and log into the vm.
1.  Once logged into the VM, you should already be in the project directory. If not, navigate to the project files with ```cd /home/vagrant/item_catalog```.
1.  Run `python setup.py` to initialize the database.
1.  (Optional) Run `python test_data.py` to populate the database with some test data to get you started.
1.  Run `python run.py` to run the flask application for the item catalog.
1.  Open a web browser and navigate to `http://localhost:5000`.

## Structure
+   itemcatalog/: Item Catalog Flask application directory.
    +   static/: Directory containing all static files.
    +   templates/: Directory containing all Jinja2 templates.
    +   __init__.py: Application definition and initialization.
    +   forms.py: WTForms declarations.
    +   helpers.py: Library of helper functions used throughout application.
    +   models.py: SQLAlchemy ORM Model declarations
    +   views.py: All views/routes used through the application.
+   instance/: Instance specific files and configuration. Excluded from repository.
    +   config.py: Instance specific configuration. Overrides values in root config.py.
    +   item_catalog.db: Default location of sqlite database
    +   images/: Default directory containing images uploaded within the Item Catalog app.
+   config.py: Flask configuration.
+   requirements.txt: Python package requirements, installed during provisioning.
+   run.py: Python file to start development server.
+   setup.py: Python file to setup fresh application/database.
+   test_data.py: Python file to setup test data for the application/database.
+   Vagrantfile: Vagrant VM configuration.
+   provision.sh: Provisioning script for the Vagrant VM. Installs the desired packages and configures the flask application.

## External Resources
+   Javascript/CSS Libraries
    1.  [Material Design Lite](http://www.getmdl.io/)
    1.  [jQuery](https://jquery.com/)
    1.  [Toastr](http://codeseven.github.io/toastr/)
+   Python Packages
    1.  Flask
    1.  SQLAlchemy
    1.  Flask-SQLAlchemy
    1.  WTForms
    1.  Flask-WTF
    1.  Flask-OAuthlib
    1.  httplib2

## Legal
Author: [W. Duncan Fraser](duncan@wduncanfraser.com)

License: [MIT License](LICENSE)