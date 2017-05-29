require 'yaml'

local_yaml = File.expand_path('../config/config.yaml', __FILE__)
options = YAML.load_file local_yaml

Vagrant.configure('2') do |config|
  config.vm.define :redis do |agent|
    agent.vm.network :forwarded_port, guest: 6379, host: 6379
    agent.vm.network :private_network, ip: options['redis::ip']
    agent.vm.box      = 'ubuntu/xenial64'
    agent.vm.hostname = 'redis'

    agent.vm.provider :virtualbox do |vbox|
      vbox.memory = 1024
    end

    agent.vm.synced_folder 'config', options['hwaas::config_dir'], create: true

    agent.vm.provision :shell, name: 'packages', inline: <<-SCRIPT
      wget https://apt.puppetlabs.com/puppetlabs-release-pc1-xenial.deb -q -P /usr/local/src
      dpkg -i /usr/local/src/puppetlabs-release-pc1-xenial.deb
      apt-get update
      apt-get install -y puppet-agent
      /opt/puppetlabs/bin/puppet module install arioch-redis --modulepath /opt/puppetlabs/puppet/modules
      cp #{options['hwaas::config_dir']}/config.yaml /etc/puppetlabs/code/environments/production/hieradata/common.yaml
    SCRIPT

    agent.vm.provision :puppet do |puppet|
      puppet.environment_path  = 'puppet/environments'
      puppet.environment       = 'production'
      puppet.manifests_path    = 'puppet/environments/production/manifests'
      puppet.manifest_file     = 'redis.pp'
      puppet.hiera_config_path = 'puppet/environments/production/hiera.yaml'
    end
  end

  config.vm.define :worker do |agent|
    agent.vm.box      = 'ubuntu/xenial64'
    agent.vm.hostname = 'worker'
    agent.vm.network :forwarded_port, guest: 9001, host: 9001
    agent.vm.network :private_network, ip: options['worker::ip']

    agent.vm.provider :virtualbox do |vbox|
      vbox.memory = 1024
    end

    agent.vm.synced_folder 'config', options['hwaas::config_dir'], create: true
    agent.vm.synced_folder '.', options['hwaas::install_dir'], create: true

    agent.vm.provision :shell, name: 'packages', inline: <<-SCRIPT
      wget https://apt.puppetlabs.com/puppetlabs-release-pc1-xenial.deb -q -P /usr/local/src
      dpkg -i /usr/local/src/puppetlabs-release-pc1-xenial.deb
      apt-get update
      apt-get install -y puppet-agent
      /opt/puppetlabs/bin/puppet module install stankevich-python --modulepath /opt/puppetlabs/puppet/modules
      /opt/puppetlabs/bin/puppet module install ajcrowe-supervisord --modulepath /opt/puppetlabs/puppet/modules
      cp #{options['hwaas::config_dir']}/config.yaml /etc/puppetlabs/code/environments/production/hieradata/common.yaml
    SCRIPT

    agent.vm.provision :puppet do |puppet|
      puppet.environment_path  = 'puppet/environments'
      puppet.environment       = 'production'
      puppet.manifests_path    = 'puppet/environments/production/manifests'
      puppet.manifest_file     = 'worker.pp'
      puppet.hiera_config_path = 'puppet/environments/production/hiera.yaml'
    end
  end

  config.vm.define :client do |agent|
    agent.vm.box      = 'ubuntu/xenial64'
    agent.vm.hostname = 'client'
    agent.vm.network :private_network, ip: options['client::ip']

    agent.vm.provider :virtualbox do |vbox|
      vbox.memory = 1024
    end

    agent.vm.synced_folder 'config', options['hwaas::config_dir'], create: true
    agent.vm.synced_folder '.', options['hwaas::install_dir'], create: true

    agent.vm.provision :shell, name: 'packages', inline: <<-SCRIPT
      wget https://apt.puppetlabs.com/puppetlabs-release-pc1-xenial.deb -q -P /usr/local/src
      dpkg -i /usr/local/src/puppetlabs-release-pc1-xenial.deb
      apt-get update
      apt-get install -y puppet-agent
      /opt/puppetlabs/bin/puppet module install stankevich-python --modulepath /opt/puppetlabs/puppet/modules
      cp #{options['hwaas::config_dir']}/config.yaml /etc/puppetlabs/code/environments/production/hieradata/common.yaml
    SCRIPT

    agent.vm.provision :puppet do |puppet|
      puppet.environment_path  = 'puppet/environments'
      puppet.environment       = 'production'
      puppet.manifests_path    = 'puppet/environments/production/manifests'
      puppet.manifest_file     = 'client.pp'
      puppet.hiera_config_path = 'puppet/environments/production/hiera.yaml'
    end
  end
end
