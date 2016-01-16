# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/centos-7.2"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.provision "shell", path: "provision.sh", :args => "item_catalog 'The item_catalog project directory is shared to the vagrant home directory, /home/vagrant/item_catalog.'"
  config.vm.synced_folder ".", "/home/vagrant/item_catalog"
end
