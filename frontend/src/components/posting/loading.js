// jshint ignore:start
import React from 'react';
import Loader from 'misago/components/loader';

export default function(props) {
  return (
    <div className="posting-ui-preview">
      <div className="container">

        <div className="row first-row">
          <div className="col-md-8">
            <input className="form-control" type="text" disabled />
          </div>
          <div className="col-md-4">
            <input className="form-control" type="text" disabled />
          </div>
        </div>

        <div className="row">
          <div className="col-md-12">
            <textarea className="form-control" rows="6" disabled></textarea>
          </div>
        </div>

      </div>
      <div className="loading-overlay">
        <div className="loading-cover">
          <div className="loading-inner">
            <Loader />
          </div>
        </div>
      </div>
    </div>
  );
}