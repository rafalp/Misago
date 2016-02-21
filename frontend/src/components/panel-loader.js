import React from 'react';
import Loader from 'misago/components/loader'; // jshint ignore:line

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="panel-body panel-body-loading">
      <Loader className="loader loader-spaced" />
    </div>;
    /* jshint ignore:end */
  }
}

