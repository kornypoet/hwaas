require 'spec_helper'

RSpec.describe package('python') do
  it { is_expected.to be_installed }
end

RSpec.describe package('puppet-agent') do
  it { is_expected.to be_installed }
end

RSpec.describe service('supervisord') do
  it { is_expected.to be_running }
end

RSpec.describe port(9001) do
  it { is_expected.to be_listening.on(local_options['worker::ip']).with('tcp') }
end

RSpec.describe file(local_options['hwaas::log_dir']) do
  it { is_expected.to be_directory }
end

RSpec.describe file(File.join(local_options['hwaas::config_dir'], 'config.yaml')) do
  it { is_expected.to exist }
end

RSpec.describe host(local_options['redis::ip']) do
  it { should be_reachable.with(port: 6379, proto: 'tcp') }
end

RSpec.describe command('hwaas -v') do
  its(:stderr) { is_expected.to match(current_version) }
end
