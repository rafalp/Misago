import React from 'react';

export default class extends React.Component {
  getEmptyMessage() {
    return interpolate(
      gettext("No users have posted any new messages during last %(days)s days."),
      {'days': this.props.trackedPeriod}, true);
  }

  render() {
    /* jshint ignore:start */
    return <div className="active-posters-list">
      <div className="container">
        <p className="lead">
          {this.getEmptyMessage()}
        </p>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}