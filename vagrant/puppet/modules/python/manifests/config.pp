class python::config {

  Class['python::install'] -> Python::Pip <| |>
  Class['python::install'] -> Python::Requirements <| |>
  Class['python::install'] -> Python::Virtualenv <| |>

  Python::Virtualenv <| |> -> Python::Pip <| |>

  if $python::gunicorn {
    Class['python::install'] -> Python::Gunicorn <| |>

    Python::Gunicorn <| |> ~> Service['gunicorn']

    service { 'gunicorn':
      ensure     => running,
      enable     => true,
      hasrestart => true,
      hasstatus  => false,
      pattern    => '/usr/bin/gunicorn',
    }
  }

}
