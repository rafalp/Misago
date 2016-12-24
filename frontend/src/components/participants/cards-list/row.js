// jshint ignore:start
import React from 'react';
import Card from './card';

export default function(props) {
  return (
    <div className="row">
      {props.participants.map((participant) => {
        return (
          <Card
            key={participant.id}
            participant={participant}
            thread={props.thread}
            user={props.user}
            userIsOwner={props.userIsOwner}
          />
        );
      })}
    </div>
  );
}