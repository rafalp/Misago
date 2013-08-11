# == Define: python::gunicorn
#
# Manages Gunicorn virtual hosts.
#
# === Parameters
#
# [*ensure*]
#  present|absent. Default: present
#
# [*virtualenv*]
#  Run in virtualenv, specify directory. Default: disabled
#
# [*mode*]
#  Gunicorn mode.
#  wsgi|django. Default: wsgi
#
# [*dir*]
#  Application directory.
#
# [*bind*]
#  Bind on: 'HOST', 'HOST:PORT', 'unix:PATH'.
#  Default: system-wide: unix:/tmp/gunicorn-$name.socket
#           virtualenv:  unix:${virtualenv}/${name}.socket
#
# [*environment*]
#  Set ENVIRONMENT variable. Default: none
#
# [*template*]
#  Which ERB template to use. Default: python/gunicorn.erb
#
# === Examples
#
# python::gunicorn { 'vhost':
#   ensure      => present,
#   virtualenv  => '/var/www/project1',
#   mode        => 'wsgi',
#   dir         => '/var/www/project1/current',
#   bind        => 'unix:/tmp/gunicorn.socket',
#   environment => 'prod',
#   template    => 'python/gunicorn.erb',
# }
#
# === Authors
#
# Sergey Stankevich
# Ashley Penney
# Marc Fournier
#
define python::gunicorn (
  $ensure        = present,
  $virtualenv    = false,
  $mode          = 'wsgi',
  $dir           = false,
  $bind          = false,
  $environment   = false,
  $template      = 'python/gunicorn.erb',
) {

  # Parameter validation
  if ! $dir {
    fail('python::gunicorn: dir parameter must not be empty')
  }

  file { "/etc/gunicorn.d/${name}":
    ensure  => $ensure,
    mode    => '0644',
    owner   => 'root',
    group   => 'root',
    content => template($template),
  }

}
