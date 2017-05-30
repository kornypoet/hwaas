require 'spec_helper'

RSpec.describe package('python') do
  it { is_expected.to be_installed }
end

RSpec.describe package('puppet-agent') do
  it { is_expected.to be_installed }
end

RSpec.describe file(File.join(local_options['hwaas::config_dir'], 'config.yaml')) do
  it { is_expected.to exist }
end

RSpec.describe host(local_options['redis::ip']) do
  it { should be_reachable.with(port: 6379, proto: 'tcp') }
end

RSpec.describe host(local_options['worker::ip']) do
  it { should be_reachable.with(port: 9001, proto: 'tcp') }
end

RSpec.describe command('hwaas -v') do
  its(:stderr) { is_expected.to match(current_version) }
end
