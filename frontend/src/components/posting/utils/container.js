// jshint ignore:start
import React from 'react';

export default function(props) {
  return (
   <div className={props.className}>
      <div className="container">
        {props.children}
      </div>
    </div>
  );
}