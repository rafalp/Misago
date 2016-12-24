// jshint ignore:start
import React from 'react';
import { changeOwner } from './actions';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.isUser = props.participant.id === props.user.id;
  }

  onClick = () => {
    let confirmed = false;
    if (this.isUser) {
      confirmed = confirm(gettext("Are you sure you want to take over this thread?"));
    } else {
      const message = gettext("Are you sure you want to change thread owner to %(user)s?");
      confirmed = confirm(interpolate(message, {
        user: this.props.participant.username
      }, true));
    }

    if (!confirmed) return;

    changeOwner(this.props.thread, this.props.participant);
  };

  render() {
    if (this.props.participant.is_owner) return null;
    if (!this.props.thread.acl.can_change_owner) return null;

    return (
      <li>
        <button type="button" onClick={this.onClick} className="btn-link btn-sm">
          {gettext("Make owner")}
        </button>
      </li>
    );
  }
}