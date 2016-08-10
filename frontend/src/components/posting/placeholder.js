// jshint ignore:start
import React from 'react';

export default function(props) {
  return (
    <div className="posting-height-placeholder container">
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
  );
}