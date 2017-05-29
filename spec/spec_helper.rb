require 'serverspec'
require 'net/ssh'
require 'tempfile'
require 'yaml'

host = ENV['RSPEC_HOST']
`vagrant up #{host}`

config = Tempfile.new('', Dir.tmpdir)
config.write(`vagrant ssh-config #{host}`)
config.close

options = Net::SSH::Config.for(host, [config.path])

set :backend, :ssh
set :host, options[:host_name]
set :ssh_options, options

RSpec.configure do
  def local_options
    local_yaml = File.expand_path('../../config/config.yaml', __FILE__)
    YAML.load_file local_yaml
  end

  def current_version
    version_file = File.expand_path('../../hwaas/version.py', __FILE__)
    File.read(version_file).match(/__version__ = '(\d+\.\d+\.\d+)'/)[1]
  end
end
