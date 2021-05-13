# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "kubmaster" do |kub|
    kub.vm.box = "bento/ubuntu-20.04"
    kub.vm.hostname = 'kubmaster'
    kub.vm.provision "docker"
    config.vm.box_url = "bento/ubuntu-20.04"

    kub.vm.network :private_network, ip: "192.168.56.101"

    kub.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 2048]
      v.customize ["modifyvm", :id, "--name", "master"]
      v.customize ["modifyvm", :id, "--cpus", "2"]
    end
  end

  config.vm.define "kubnode1" do |kubnode|
    kubnode.vm.box = "bento/ubuntu-20.04"
    kubnode.vm.hostname = 'kubnode1'
    kubnode.vm.provision "docker"
    config.vm.box_url = "bento/ubuntu-20.04"

    kubnode.vm.network :private_network, ip: "192.168.56.102"

    kubnode.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 2048]
      v.customize ["modifyvm", :id, "--name", "kubnode1"]
      v.customize ["modifyvm", :id, "--cpus", "2"]
    end
  end

  config.vm.define "kubnode2" do |kubnode|
    kubnode.vm.box = "bento/ubuntu-20.04"
    kubnode.vm.hostname = 'kubnode2'
    kubnode.vm.provision "docker"
    config.vm.box_url = "bento/ubuntu-20.04"

    kubnode.vm.network :private_network, ip: "192.168.56.103"

    kubnode.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 2048]
      v.customize ["modifyvm", :id, "--name", "kubnode2"]
      v.customize ["modifyvm", :id, "--cpus", "2"]
    end
  end
end

