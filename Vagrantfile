Vagrant.configure('2') do |config|
  config.vm.define :hwaas do |agent|
    agent.vm.box      = 'ubuntu/xenial64'
    agent.vm.hostname = 'hello-world-server'

    agent.vm.provider :virtualbox do |vbox|
      vbox.memory = 4096
    end

    agent.vm.provision :shell, name: 'packages', inline: <<-SCRIPT
      wget https://apt.puppetlabs.com/puppetlabs-release-pc1-xenial.deb -q -P /usr/local/src
      dpkg -i /usr/local/src/puppetlabs-release-pc1-xenial.deb
      apt-get update
      apt-get install -y redis-server python python-setuptools puppet-agent
      /opt/puppetlabs/bin/puppet module install ajcrowe-supervisord --modulepath /opt/puppetlabs/puppet/modules
    SCRIPT

    agent.vm.provision :shell, name: 'install', inline: <<-SCRIPT
      cd /vagrant
      python setup.py install
    SCRIPT

    agent.vm.provision :puppet do |puppet|
      puppet.environment_path = 'environments'
      puppet.environment      = 'production'
    end
  end
end
