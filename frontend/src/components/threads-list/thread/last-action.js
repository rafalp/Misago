/* jshint ignore:start */
import React from 'react';
import Avatar from 'misago/components/avatar';
import UserUrl from './user-url';

export default function({ thread }) {
  return (
    <div className="media">
      <div className="media-left">
        <UserUrl
          className="thread-last-poster-avatar"
          url={thread.url.last_poster}
        >
          <Avatar
            className="media-object"
            size={40}
            user={thread.last_poster}
          />
        </UserUrl>
      </div>
      <div className="media-body">
        <UserUrl
          className="item-title thread-last-poster"
          url={thread.url.last_poster}
        >
          {thread.last_poster_name}
        </UserUrl>
        <Timestamp
          datetime={thread.last_post_on}
          url={thread.url.last_post}
        />
      </div>
    </div>
  );
}

export function Timestamp({ datetime, url }) {
  return (
    <a
      className="thread-last-reply"
      href={url}
      title={datetime.format('LLL')}
    >
      {datetime.fromNow(true)}
    </a>
  );
}