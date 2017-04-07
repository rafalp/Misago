// jshint ignore:start
import React from 'react';
import MakeOwner from './make-owner';
import Remove from './remove';
import Avatar from 'misago/components/avatar';

export default function(props) {
  const participant = props.participant;

  return (
    <div className="col-xs-12 col-sm-6 col-md-3 participant-card">
      <a className="avatar-link" href={participant.url}>
        <Avatar user={participant} size="50" />
      </a>
      <div className="participant-profile">
        <a className="item-title" href={participant.url}>
          {participant.username}
        </a>
        <ul className="list-unstyled list-inline">
          <OwnerBadge {...participant} />
          <MakeOwner {...props} />
          <Remove {...props} />
        </ul>
      </div>
    </div>
  );
}

export function OwnerBadge(props) {
  if (!props.is_owner) return null;

  return (
    <li className="participant-owner">
      <span className="material-icon">
        grade
      </span>
      {gettext("Owner")}
    </li>
  );
}