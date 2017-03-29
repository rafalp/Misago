/* jshint ignore:start */
import React from 'react';
import Pager from 'misago/components/users/rank/pager';
import UsersList from 'misago/components/users-list/root';

export default function(props) {
  return (
    <div>
      <UsersList
        cols={3}
        isLoaded={true}
        showStatus={true}
        users={props.users}
      />
      <Pager {...props} />
    </div>
  );
}