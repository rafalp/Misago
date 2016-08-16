// jshint ignore:start
import React from 'react';
import Filler from './filler';

export default function(props) {
  return (
   <div className={props.className}>
      <Filler withFirstRow={props.withFirstRow} />

      <div className="posting-overlay">
        <div className="posting-cover">
          <div className="posting-inner">

            <div className="container">
              {props.children}
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}