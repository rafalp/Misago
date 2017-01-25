// jshint ignore:start
import React from 'react';
import Row from './row';
import batch from 'misago/utils/batch';

export default function(props) {
  return (
    <div className="participants-cards">
      {batch(props.participants, 4).map((row) => {
        const key = row.map((i) => i.id).join('_');
        return (
          <Row
            key={key}
            participants={row}
            thread={props.thread}
            user={props.user}
            userIsOwner={props.userIsOwner}
          />
        );
      })}
    </div>
  );
}