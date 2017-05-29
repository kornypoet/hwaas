$install_dir = lookup('hwaas::install_dir')

class { 'python':
  version => 'system',
  pip     => 'latest',
}

exec { 'install hwaas':
  command => '/usr/bin/python setup.py install',
  cwd     => $install_dir,
}
