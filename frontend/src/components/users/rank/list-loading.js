import React from 'react';
import UsersList from 'misago/components/users-list' // jshint ignore:line

export default class extends React.Component {
  shouldComponentUpdate() {
    return false;
  }

  render() {
    /* jshint ignore:start */
    return (
      <div>
        <UsersList
          cols={4}
          isReady={false}
        />
      </div>
    );
    /* jshint ignore:end */
  }
}
