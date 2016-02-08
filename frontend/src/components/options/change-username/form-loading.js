import React from 'react';
import Loader from 'misago/components/loader'; // jshint ignore:line

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="panel panel-default panel-form">
      <div className="panel-heading">
        <h3 className="panel-title">{gettext("Change username")}</h3>
      </div>
      <div className="panel-body panel-body-loading">

        <Loader className="loader loader-spaced" />

      </div>
    </div>;
    /* jshint ignore:end */
  }
}