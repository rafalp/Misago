import React from 'react';

export default class extends React.Component {
  render () {
    if (this.props.list.type === 'all') {
      if (this.props.emptyMessage) {
        /* jshint ignore:start */
        return (
          <li className="list-group-item empty-message">
            <p className="lead">
              {this.props.emptyMessage}
            </p>
            <p>
              {gettext("Why not start one yourself?")}
            </p>
          </li>
        );
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return (
          <li className="list-group-item empty-message">
            <p className="lead">
              {this.props.category.special_role
                ? gettext("There are no threads on this forum... yet!")
                : gettext("There are no threads in this category.")}
            </p>
            <p>
              {gettext("Why not start one yourself?")}
            </p>
          </li>
        );
        /* jshint ignore:end */
      }
    } else {
      /* jshint ignore:start */
      return <li className="list-group-item empty-message">
        {gettext("No threads matching specified criteria were found.")}
      </li>;
      /* jshint ignore:end */
    }
  }
}