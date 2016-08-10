// jshint ignore:start
import React from 'react';
import Placeholder from './placeholder';
import Loader from 'misago/components/loader';
import posting from 'misago/services/posting';

export default function(props) {
  return (
    <div className="posting-message">

      <Placeholder />

      <div className="posting-overlay">
        <div className="posting-cover">
          <div className="posting-inner">
            <div className="container">

              <div className="message-body">
                <p>
                  <span className="material-icon">
                    error_outline
                  </span>
                  {props.message}
                </p>
                <button type="button" className="btn btn-default" onClick={posting.close}>
                  {gettext("Dismiss")}
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>

    </div>
  );
}