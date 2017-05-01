/* jshint ignore:start */
import React from 'react';
import Avatar from 'misago/components/avatar';
import UserStatus, { StatusIcon, StatusLabel } from 'misago/components/user-status';
import UserPostcount from './user-postcount';
import UserTitle from './user-title';

export default function({ post }) {
  const { poster } = post;

  return (
    <div className="col-md-3 post-side post-side-registered">
      <div className="media">
        <div className="media-left">
          <a href={poster.absolute_url}>
            <Avatar
              className="poster-avatar"
              size={100}
              user={poster}
            />
          </a>
        </div>
        <div className="media-body">

          <a
            className="media-heading item-title"
            href={poster.absolute_url}
          >
            {poster.username}
          </a>

          <UserTitle
            rank={poster.rank}
            title={poster.title}
          />

          <UserStatus status={poster.status}>
            <StatusLabel
              status={poster.status}
              user={poster}
            />
          </UserStatus>

          <UserPostcount poster={poster} />

        </div>
      </div>
    </div>
  );
}