require 'serverspec'
require 'net/ssh'
require 'tempfile'

`vagrant up hwaas`

config = Tempfile.new('', Dir.tmpdir)
config.write(`vagrant ssh-config hwaas`)
config.close

options = Net::SSH::Config.for('hwaas', [config.path])

set :backend, :ssh
set :host, options[:host_name]
set :ssh_options, options
