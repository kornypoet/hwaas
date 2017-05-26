class { 'supervisord':
  install_pip          => true,
  unix_socket          => false,
  inet_server          => true,
  inet_server_hostname => '127.0.0.1',
  inet_server_port     => '9001',
  inet_auth            => false,
  inet_username        => undef,
  inet_password        => undef,
}
