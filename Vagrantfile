# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "quantal-server"
  config.vm.box_url = "http://static.aldoborrero.com/vagrant/quantal64.box"
  config.vm.network :forwarded_port, guest: 80, host: 8080
  config.vm.synced_folder "server/app", "/opt/water/app"

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1536"]
  end

  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = "./provisioning/cookbooks"
    chef.roles_path = "./provisioning/roles"
    chef.data_bags_path = "./provisioning/data_bags"
    chef.add_role "ubuntu"
    chef.add_role "safewater-dev"

    # You may also specify custom JSON attributes:
    # chef.json = { :mysql_password => "foo" }

  end

end
