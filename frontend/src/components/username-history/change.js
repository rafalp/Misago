import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line

export default class extends React.Component {
  renderUserAvatar() {
    if (this.props.change.changed_by) {
      /* jshint ignore:start */
      return <a href={this.props.change.changed_by.absolute_url} className="user-avatar-wrapper">
        <Avatar user={this.props.change.changed_by} size="100" />
      </a>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <span className="user-avatar-wrapper">
        <Avatar size="100" />
      </span>;
      /* jshint ignore:end */
    }
  }

  renderUsername() {
    if (this.props.change.changed_by) {
      /* jshint ignore:start */
      return <a href={this.props.change.changed_by.absolute_url} className="item-title">
        {this.props.change.changed_by.username}
      </a>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <span className="item-title">
        {this.props.change.changed_by_username}
      </span>;
      /* jshint ignore:end */
    }
  }

  render() {
    /* jshint ignore:start */
    return <li className="list-group-item" key={this.props.change.id}>
      <div className="change-avatar">
        {this.renderUserAvatar()}
      </div>
      <div className="change-author">
        {this.renderUsername()}
      </div>
      <div className="change">
        <span className="old-username">
          {this.props.change.old_username}
        </span>
        <span className="material-icon">
          arrow_forward
        </span>
        <span className="new-username">
          {this.props.change.new_username}
        </span>
      </div>
      <div className="change-date">
        <abbr title={this.props.change.changed_on.format('LLL')}>
          {this.props.change.changed_on.fromNow()}
        </abbr>
      </div>
    </li>;
    /* jshint ignore:end */
  }
}