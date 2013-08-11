# == Define: python::requirements
#
# Installs and manages Python packages from requirements file.
#
# === Parameters
#
# [*requirements*]
#  Path to the requirements file. Defaults to the resource name
#
# [*virtualenv*]
#  virtualenv to run pip in. Default: system-wide
#
# [*owner*]
#  The owner of the virtualenv being manipulated. Default: root
#
# [*group*]
#  The group relating to the virtualenv being manipulated. Default: root
#
# [*proxy*]
#  Proxy server to use for outbound connections. Default: none
#
# [*environment*]
#  Additional environment variables required to install the packages. Default: none
#
# === Examples
#
# python::requirements { '/var/www/project1/requirements.txt':
#   virtualenv => '/var/www/project1',
#   proxy      => 'http://proxy.domain.com:3128',
# }
#
# === Authors
#
# Sergey Stankevich
# Ashley Penney
# Fotis Gimian
#
define python::requirements (
  $requirements = $name,
  $virtualenv   = 'system',
  $owner        = 'root',
  $group        = 'root',
  $proxy        = false,
  $environment = []
) {

  if $virtualenv == 'system' and ($owner != 'root' or $group != 'root') {
    fail('python::pip: root user must be used when virtualenv is system')
  }

  $cwd = $virtualenv ? {
    'system' => '/',
    default  => "${virtualenv}",
  }

  $pip_env = $virtualenv ? {
    'system' => 'pip',
    default  => "${virtualenv}/bin/pip",
  }

  $proxy_flag = $proxy ? {
    false    => '',
    default  => "--proxy=${proxy}",
  }

  # This will ensure multiple python::virtualenv definitions can share the
  # the same requirements file.
  if !defined(File[$requirements]) {
    file { $requirements:
      ensure  => present,
      mode    => '0644',
      owner   => $owner,
      group   => $group,
      audit   => content,
      replace => false,
      content => '# Puppet will install and/or update pip packages listed here',
    }
  }

  exec { "python_requirements${name}":
    provider    => shell,
    command     => "${pip_env} --log-file ${cwd}/pip.log install ${proxy_flag} -r ${requirements}",
    refreshonly => true,
    timeout     => 1800,
    user        => $owner,
    subscribe   => File[$requirements],
    environment => $environment,
  }

}
