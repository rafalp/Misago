// jshint ignore:start
import React from 'react';
import CardsList from './cards-list';
import * as utils from './utils';

export default function(props) {
  if (!props.participants.length) return null;

  return (
    <div className="panel panel-default panel-participants">
      <div className="panel-body">
        <CardsList
          userIsOwner={getUserIsOwner(props.user, props.participants)}
          {...props}
        />
        <p>{utils.getParticipantsCopy(props.participants)}</p>
      </div>
    </div>
  );
}

export function getUserIsOwner(user, participants) {
  return participants[0].id === user.id
}