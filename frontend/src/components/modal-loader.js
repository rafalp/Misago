import React from 'react';
import Loader from 'misago/components/loader'; // jshint ignore:line

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="modal-body modal-loader">
      <Loader />
    </div>;
    /* jshint ignore:end */
  }
}

