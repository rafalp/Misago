/* jshint ignore:start */
import React from 'react';
import Header from './header';
import misago from 'misago';

const Complete = ({ activation, backend_name, username }) => {
  let icon = '';
  let message = '';
  if (activation === 'user') {
    message = gettext("%(username)s, your account has been created but you need to activate it before you will be able to sign in.");
  } else if (activation === 'admin') {
    message = gettext("%(username)s, your account has been created but board administrator will have to activate it before you will be able to sign in.");
  } else {
    message = gettext("%(username)s, your account has been created and you have been signed in to it.")
  }

  if (activation === 'active') {
    icon = 'check';
  } else {
    icon = 'info_outline';
  }

  return (
    <div className="page page-social-auth page-social-sauth-register">
      <Header backendName={backend_name} />
      <div className="container">
        <div className="row">
          <div className="col-md-6 col-md-offset-3">

            <div className="panel panel-default panel-form">
              <div className="panel-heading">
                <h3 className="panel-title">{gettext("Registration completed!")}</h3>
              </div>
              <div className="panel-body panel-message-body">
                <div className="message-icon">
                  <span className="material-icon">
                    {icon}
                  </span>
                </div>
                <div className="message-body">
                  <p className="lead">
                    {interpolate(message, { username }, true)}
                  </p>
                  <p className="help-block">
                    <a
                      className="btn btn-default"
                      href={misago.get('MISAGO_PATH')}
                    >
                      {gettext("Return to forum index")}
                    </a>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Complete;