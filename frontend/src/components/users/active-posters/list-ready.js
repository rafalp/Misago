import React from 'react';
import ListItem from 'misago/components/users/active-posters/list-item'; // jshint ignore:line

export default class extends React.Component {
  getLeadMessage() {
    let message = ngettext(
        "%(posters)s most active poster from last %(days)s days.",
        "%(posters)s most active posters from last %(days)s days.",
        this.props.count);

    return interpolate(message, {
      posters: this.props.count,
      days: this.props.trackedPeriod
    }, true);
  }

  render() {
    /* jshint ignore:start */
    return <div className="active-posters-list">
      <div className="container">
        <p className="lead">
          {this.getLeadMessage()}
        </p>

        <div className="active-posters ui-ready">
          <ul className="list-group">
            {this.props.users.map((user, i) => {
              return <ListItem user={user}
                               rank={user.rank}
                               counter={i + 1}
                               key={user.id} />;
            })}
          </ul>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}