import React from 'react';
import ListItem from 'misago/components/users/rank/list-item' // jshint ignore:line
import Pager from 'misago/components/users/rank/pager' // jshint ignore:line
import batch from 'misago/utils/batch'; // jshint ignore:line

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
      <div className="users-cards-list ui-ready">
        {batch(this.props.users, 3).map((row, r) => {
          return <div className="row" key={r}>
            {row.map((user) => {
              return <div className="col-md-4" key={user.id}>
                <ListItem user={user} />
              </div>;
            })}
          </div>;
        })}
      </div>
      {this.getPager()}
    </div>;
    /* jshint ignore:end */
  }
}