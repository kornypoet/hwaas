class { '::redis':
  bind => lookup('redis::ip'),
}
