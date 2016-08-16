// jshint ignore:start
import React from 'react';
import Editor from 'misago/components/editor'; //jshint ignore:line

export default function(props) {
  return (
    <div className="posting-height-filler container">
      <FirstRow visible={props.withFirstRow} />
      <div className="row">
        <div className="col-md-12">
          <Editor />
        </div>
      </div>
    </div>
  );
}

export function FirstRow(props) {
  if (props.visible) {
    return (
      <div className="row first-row">
        <div className="col-md-8">
          <input className="form-control" type="text" disabled />
        </div>
        <div className="col-md-4">
          <input className="form-control" type="text" disabled />
        </div>
      </div>
    );
  } else {
    return null;
  }
}