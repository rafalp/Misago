// jshint ignore:start
import React from 'react';
import Placeholder from './placeholder';
import Loader from 'misago/components/loader';

export default function(props) {
  return (
    <div className="posting-loader">

      <Placeholder />

      <div className="posting-overlay">
        <div className="posting-cover">
          <div className="posting-inner">
            <div className="container">

              <Loader />

            </div>
          </div>
        </div>
      </div>

    </div>
  );
}