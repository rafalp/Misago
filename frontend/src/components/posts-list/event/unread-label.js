/* jshint ignore:start */
import React from 'react';

export default function({ post }) {
  if (post.is_read) return null;

  return (
    <div className="row">
      <div className="col-xs-10 col-xs-offset-2 col-sm-9 col-sm-offset-3 text-left">

        <div className="event-label">
          <span className="label label-unread">
            {gettext("New event")}
          </span>
        </div>

      </div>
    </div>
  );
}