/* jshint ignore:start */
import React from 'react';

export default function({ isAuthenticated, profile }) {
  let message = null;
  if (isAuthenticated) {
    message = gettext("You are not sharing any details with others.");
  } else {
    message = interpolate(
      gettext("%(username)s is not sharing any details with others."),
      {
        'username': profile.username,
      },
      true
    );
  }

  return (
    <div className="panel panel-default">
      <div className="panel-body text-center lead">
        {message}
      </div>
    </div>
  );
}