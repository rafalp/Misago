/* jshint ignore:start */
import React from 'react';
import ReplyButton from './reply-button';
import Subscription from './subscription';

export default function(props) {
  return (
    <div className="toolbar">
      <ul className="list-inline">
        <GotoNew thread={props.thread} />
        <GotoUnapproved thread={props.thread} />
        <GotoLast thread={props.thread} />
        <Reply openReplyForm={props.openReplyForm} thread={props.thread} />
        <SubscriptionMenu {...props} />
      </ul>
    </div>
  );
}

export function GotoNew(props) {
  if (props.thread.is_new) {
    return (
      <li>
        <a href={props.thread.url.new_post} className="btn btn-default" title={gettext('Go to first new post')}>
          {gettext("New")}
        </a>
      </li>
    );
  } else {
    return null;
  }
}

export function GotoUnapproved(props) {
  if (props.thread.has_unapproved_posts && props.thread.acl.can_approve) {
    return (
      <li>
        <a href={props.thread.url.unapproved_post} className="btn btn-default" title={gettext('Go to first unapproved post')}>
          {gettext("Unapproved")}
        </a>
      </li>
    );
  } else {
    return null;
  }
}

export function GotoLast(props) {
  return (
    <li>
      <a href={props.thread.url.last_post} className="btn btn-default" title={gettext('Go to last post')}>
        {gettext("Last")}
      </a>
    </li>
  );
}

export function SubscriptionMenu(props) {
  if (!props.user.id) {
    return null;
  }

  return (
    <li className="pull-right">
      <Subscription className="dropdown toolbar-right" {...props} />
    </li>
  )
}

export function Reply(props) {
  if (props.thread.acl.can_reply) {
    return (
      <li className="pull-right">
        <ReplyButton onClick={props.openReplyForm} />
      </li>
    );
  } else {
    return null;
  }
}