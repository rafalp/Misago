# Class: site
#
#
class site
{
  $login    = "Admin"
  $email    = "admin@example.com"
  $password = "password"

  class { "python":
    version => "system",
    dev     => true
  } ->

  python::requirements { "/vagrant/requirements.txt":
    virtualenv => "system"
  } ->

  exec { "startmisago":
    command => "python manage.py startmisago",
    path    => "/usr/bin:/usr/sbin:/bin:/usr/local/bin",
    cwd     => "/vagrant"
  } ->

  exec { "adduser":
    command => "python manage.py adduser ${login} ${email} ${password} --admin \
               && /bin/echo 'admin_user_created' >> /etc/puppet/puppet_history",
    unless  => "/bin/grep 'admin_user_created' /etc/puppet/puppet_history",
    path    => "/usr/bin:/usr/sbin:/bin:/usr/local/bin",
    cwd     => "/vagrant"
  }
}

include site
