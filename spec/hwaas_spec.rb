require 'spec_helper'

version_file = File.expand_path('../../hwaas/version.py', __FILE__)
current_version = File.read(version_file).match(/__version__ = '(\d+\.\d+\.\d+)'/)[1]

RSpec.describe package('redis-server') do
  it { is_expected.to be_installed }
end

RSpec.describe package('python') do
  it { is_expected.to be_installed }
end

RSpec.describe package('python-setuptools') do
  it { is_expected.to be_installed }
end

RSpec.describe package('puppet-agent') do
  it { is_expected.to be_installed }
end

RSpec.describe service('redis-server') do
  it { is_expected.to be_running }
end

RSpec.describe service('supervisord') do
  it { is_expected.to be_running }
end

describe port(9001) do
  it { is_expected.to be_listening.on('127.0.0.1').with('tcp') }
end

RSpec.describe command('hwaas -v') do
  its(:stderr) { is_expected.to match(current_version) }
end
