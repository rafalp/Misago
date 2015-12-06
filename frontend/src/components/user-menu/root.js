import React from 'react';
import mount from 'misago/utils/mount-component';

class UserMenu extends React.Component {
  render() {
    /* jshint ignore:start */
    return <p>{'Hello, <b>world</b>!'}</p>;
    /* jshint ignore:end */
  }
}

mount(UserMenu, 'user-menu-mount');
