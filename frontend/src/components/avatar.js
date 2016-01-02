import React from 'react';

const BASE_URL = $('base').attr('href') + 'user-avatar/';

export default class extends React.Component {
  getSrc() {
    let size = this.props.size || 100; // jshint ignore:line
    let url = BASE_URL;

    if (this.props.user && this.props.user.id) {
      // just avatar hash, size and user id
      url += this.props.user.avatar_hash + '/' + size + '/' + this.props.user.id + '.png';
    } else {
      // just append avatar size to file to produce no-avatar placeholder
      url += size + '.png';
    }

    return url;
  }

  render() {
    /* jshint ignore:start */
    return <img src={this.getSrc()}
                className={this.props.className || 'user-avatar'}
                title={gettext("User avatar")}/>;
    /* jshint ignore:end */
  }
}
