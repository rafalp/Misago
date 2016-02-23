import React from 'react';
import Pager from 'misago/components/users/rank/pager' // jshint ignore:line
import UsersList from 'misago/components/users-list/root' // jshint ignore:line

export default class extends React.Component {
  getPager() {
    if (this.props.pages > 1) {
      /* jshint ignore:start */
      return <Pager {...this.props} />
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div>
      <UsersList users={this.props.users}
                 showStatus={true}
                 cols={3}
                 isLoaded={true} />

      {this.getPager()}
    </div>;
    /* jshint ignore:end */
  }
}