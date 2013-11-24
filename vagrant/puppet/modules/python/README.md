[puppet-python](https://github.com/stankevich/puppet-python)
======

Puppet module for installing and managing python, pip, virtualenvs and Gunicorn virtual hosts.

**Version 1.1.x Notes**

Version 1.1.x makes several fundamental changes to the core of this module, adding some additional features, improving performance and making operations more robust in general.

Please note that everal changes have been made in v1.1.x which make manifests incompatible with the previous version.  However, modifying your manifests to suit is trivial.  Please see the notes below.

Currently, the changes you need to make are as follows:

* All pip definitions MUST include the owner field which specifies which user owns the virtualenv that packages will be installed in.  Adding this greatly improves performance and efficiency of this module.
* You must explicitly specify pip => true in the python class if you want pip installed.  As such, the pip package is now independent of the dev package and so one can exist without the other.

## Installation

``` bash
cd /etc/puppet/modules
git clone git://github.com/stankevich/puppet-python.git python
```

## Usage

### python

Installs and manages python, python-dev, python-virtualenv and Gunicorn.

**version** - Python version to install. Default: system default

**pip** - Install python-pip. Default: false

**dev** - Install python-dev. Default: false

**virtualenv** - Install python-virtualenv. Default: false

**gunicorn** - Install Gunicorn. Default: false

	class { 'python':
	  version    => 'system',
	  dev        => true,
	  virtualenv => true,
	  gunicorn   => true,
	}

### python::pip

Installs and manages packages from pip.

**ensure** - present/absent. Default: present

**virtualenv** - virtualenv to run pip in. Default: system (no virtualenv)

**url** - URL to install from. Default: none

**owner** - The owner of the virtualenv to ensure that packages are installed with the correct permissions (must be specified). Default: root

**proxy** - Proxy server to use for outbound connections. Default: none

**environment** - Additional environment variables required to install the packages. Default: none

	python::pip { 'cx_Oracle':
	  virtualenv  => '/var/www/project1',
	  owner       => 'appuser',
	  proxy       => 'http://proxy.domain.com:3128',
	  environment => 'ORACLE_HOME=/usr/lib/oracle/11.2/client64',
	}

### python::requirements

Installs and manages Python packages from requirements file.

**virtualenv** - virtualenv to run pip in. Default: system-wide

**proxy** - Proxy server to use for outbound connections. Default: none

**owner** - The owner of the virtualenv to ensure that packages are installed with the correct permissions (must be specified). Default: root

**group** - The group that was used to create the virtualenv.  This is used to create the requirements file with correct permissions if it's not present already.

	python::requirements { '/var/www/project1/requirements.txt':
	  virtualenv => '/var/www/project1',
	  proxy      => 'http://proxy.domain.com:3128',
	  owner      => 'appuser',
	  group      => 'apps',
	}

### python::virtualenv

Creates Python virtualenv.

**ensure** - present/absent. Default: present

**version** - Python version to use. Default: system default

**requirements** - Path to pip requirements.txt file. Default: none

**proxy** - Proxy server to use for outbound connections. Default: none

**systempkgs** - Copy system site-packages into virtualenv. Default: don't

**distribute** - Include distribute in the virtualenv. Default: true

**owner** - Specify the owner of this virtualenv

**group** - Specify the group for this virtualenv

**index** - Base URL of Python package index. Default: none

	python::virtualenv { '/var/www/project1':
	  ensure       => present,
	  version      => 'system',
	  requirements => '/var/www/project1/requirements.txt',
	  proxy        => 'http://proxy.domain.com:3128',
	  systempkgs   => true,
	  distribute   => false,
	  owner        => 'appuser',
	  group        => 'apps',
	}

### python::gunicorn

Manages Gunicorn virtual hosts.

**ensure** - present/absent. Default: present

**virtualenv** - Run in virtualenv, specify directory. Default: disabled

**mode** - Gunicorn mode. wsgi/django. Default: wsgi

**dir** - Application directory.

**bind** - Bind on: 'HOST', 'HOST:PORT', 'unix:PATH'. Default: unix:/tmp/gunicorn-$name.socket or unix:${virtualenv}/${name}.socket

**environment** - Set ENVIRONMENT variable. Default: none

**template** - Which ERB template to use. Default: python/gunicorn.erb

	python::gunicorn { 'vhost':
	  ensure      => present,
	  virtualenv  => '/var/www/project1',
	  mode        => 'wsgi',
	  dir         => '/var/www/project1/current',
	  bind        => 'unix:/tmp/gunicorn.socket',
	  environment => 'prod',
	  template    => 'python/gunicorn.erb',
	}

## Authors

[Sergey Stankevich](https://github.com/stankevich)
[Ashley Penney](https://github.com/apenney)
[Marc Fournier](https://github.com/mfournier)
[Fotis Gimian](https://github.com/fgimian)
