// jshint ignore:start
import React from 'react';
import Container from './container';
import posting from 'misago/services/posting';

export default function(props) {
  return (
    <Container className="posting-message">
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
    </Container>
  );
}