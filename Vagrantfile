Vagrant.configure('2') do |config|
  config.vm.define :hello_world do |agent|
    agent.vm.box      = 'ubuntu/xenial64'
    agent.vm.hostname = 'hello-world-server'

    agent.vm.provision :shell, name: 'packages', inline: <<-SCRIPT
      apt-get update
      apt-get install -y redis-server python python-setuptools
    SCRIPT

    agent.vm.provision :shell, name: 'install hwaas', inline: <<-SCRIPT
      cd /vagrant
      python setup.py install
    SCRIPT
  end
end
