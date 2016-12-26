/* jshint ignore:start */
import React from 'react';
import Breadcrumbs from './breadcrumbs';
import { isModerationVisible, ModerationControls } from '../moderation/thread';
import Stats from './stats';
import Title from './title';

export default function(props) {
  return <div className="page-header with-stats with-breadcrumbs">
    <Breadcrumbs path={props.thread.path} />
    <div className="container">
      <div className="row">
        <div className="col-md-10">
          <Title thread={props.thread} user={props.user} />
        </div>
        <div className="col-md-2">
          <Moderation
            posts={props.posts}
            thread={props.thread}
            user={props.user}
          />
        </div>
      </div>
    </div>
    <Stats thread={props.thread} />
  </div>;
}

export function Moderation(props) {
  if (props.user.id && isModerationVisible(props.thread)) {
    return (
      <div className="btn-group pull-right">
        <button
          aria-expanded="false"
          aria-haspopup="true"
          className="btn btn-default dropdown-toggle"
          data-toggle="dropdown"
          disabled={props.thread.isBusy}
          type="button"
        >
          <span className="material-icon">
            settings
          </span>
          {gettext("Moderation")}
        </button>
        <ModerationControls
          posts={props.posts}
          thread={props.thread}
          user={props.user}
        />
      </div>
    )
  } else {
    return null;
  }
}