require 'rspec/core/rake_task'

task default: 'spec:all'

hosts = [
  :redis
]

namespace :spec do
  desc 'Run all specs for all hosts'
  task all: hosts.map{ |host| ['spec', host].join(':') }

  hosts.each do |host|
    desc "Run specs for #{host} host"
    RSpec::Core::RakeTask.new(host) do |t|
      ENV['RSPEC_HOST'] = host.to_s
      t.pattern = "spec/#{host}_spec.rb"
    end
  end
end
