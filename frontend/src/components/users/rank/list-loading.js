import React from 'react';
import UsersList from 'misago/components/users-list/root' // jshint ignore:line

export default class extends React.Component {
  shouldComponentUpdate() {
    return false;
  }

  render() {
    /* jshint ignore:start */
    return <div>
      <UsersList isLoaded={false} cols={3} showStatus={true} />
    </div>;
    /* jshint ignore:end */
  }
}
