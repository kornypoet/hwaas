require 'spec_helper'

RSpec.describe package('puppet-agent') do
  it { is_expected.to be_installed }
end

RSpec.describe package('redis-server') do
  it { is_expected.to be_installed }
end

RSpec.describe service('redis-server') do
  it { is_expected.to be_running }
end

RSpec.describe port(6379) do
  it { is_expected.to be_listening.on(local_options['redis::ip']).with('tcp') }
end
