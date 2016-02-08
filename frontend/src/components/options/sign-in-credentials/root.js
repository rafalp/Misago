import React from 'react';
import ChangeEmail from 'misago/components/options/sign-in-credentials/change-email'; // jshint ignore:line
import ChangePassword from 'misago/components/options/sign-in-credentials/change-password'; // jshint ignore:line
import misago from 'misago/index'; // jshint ignore:line
import title from 'misago/services/page-title';

export default class extends React.Component {
  componentDidMount() {
    title.set({
      title: gettext("Change email or password"),
      parent: gettext("Change your options")
    });
  }

  render() {
    /* jshint ignore:start */
    return <div>
      <ChangeEmail user={this.props.user} />
      <ChangePassword user={this.props.user} />

      <p className="message-line">
        <span className="material-icon">
          warning
        </span>
        <a href={misago.get('FORGOTTEN_PASSWORD_URL')}>
          {gettext("Change forgotten password")}
        </a>
      </p>
    </div>
    /* jshint ignore:end */
  }
}