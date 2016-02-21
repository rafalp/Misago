import React from 'react';
import PanelLoader from 'misago/components/panel-loader'; // jshint ignore:line

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="panel panel-default panel-form">
      <div className="panel-heading">
        <h3 className="panel-title">{gettext("Change username")}</h3>
      </div>

      <PanelLoader />

    </div>;
    /* jshint ignore:end */
  }
}