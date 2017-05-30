$install_dir = lookup('hwaas::install_dir')
$log_dir = lookup('hwaas::log_dir')

class { 'python':
  version => 'system',
  pip     => 'latest',
}

exec { 'install hwaas':
  command => '/usr/bin/python setup.py install',
  cwd     => $install_dir,
}

class { 'supervisord':
  install_pip          => false,
  unix_socket          => false,
  inet_server          => true,
  inet_server_hostname => lookup('worker::ip'),
  inet_server_port     => '9001',
  inet_auth            => false,
  inet_username        => undef,
  inet_password        => undef,
}

file { $log_dir:
  ensure => directory,
}

supervisord::group { 'hwaas':
  programs => [],
}

package { 'supervisor_twiddler':
  provider => pip,
}

supervisord::rpcinterface { 'twiddler':
  rpcinterface_factory => 'supervisor_twiddler.rpcinterface:make_twiddler_rpcinterface',
  require => Package['supervisor_twiddler'],
  notify  => Exec['restart supervisor for rpc interface'],
}

exec { 'restart supervisor for rpc interface':
  command     => "/usr/sbin/service ${::supervisord::service_name} restart",
  refreshonly => true
}
