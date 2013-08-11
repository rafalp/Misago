# Rakefile for puppet-lint (https://github.com/rodjek/puppet-lint)
# Run: rake lint

require 'puppet-lint/tasks/puppet-lint'
PuppetLint.configuration.with_filename = true
PuppetLint.configuration.send('disable_documentation')
PuppetLint.configuration.send('disable_class_parameter_defaults')
PuppetLint.configuration.send('disable_80chars')
