/* jshint ignore:start */
import React from 'react';
import escapeHtml from 'misago/utils/escape-html';

const LAST_POSTER_URL = '<a href="%(url)s" class="poster-title">%(user)s</a>';
const LAST_POSTER_SPAN = '<span class="poster-title">%(user)s</span>';
const LAST_REPLY_URL = '<abbr class="last-title" title="%(absolute)s">%(relative)s</abbr>';

export function Weight(props) {
  if (props.thread.weight == 2) {
    return <li className="thread-pinned-globally">
      <span className="material-icon">
        bookmark
      </span>
      <span className="icon-legend">
        {gettext("Pinned globally")}
      </span>
    </li>;
  } else if (props.thread.weight == 2) {
    return <li className="thread-pinned-locally">
      <span className="material-icon">
        bookmark_border
      </span>
      <span className="icon-legend">
        {gettext("Pinned locally")}
      </span>
    </li>;
  } else {
    return null;
  }
}

export function Unapproved(props) {
  if (props.thread.is_unapproved) {
    return <li className="thread-unapproved">
      <span className="material-icon">
        remove_circle
      </span>
      <span className="icon-legend">
        {gettext("Unapproved")}
      </span>
    </li>;
  } else if (props.thread.has_unapproved_posts) {
    return <li className="thread-unapproved-posts">
      <span className="material-icon">
        remove_circle_outline
      </span>
      <span className="icon-legend">
        {gettext("Unapproved posts")}
      </span>
    </li>;
  } else {
    return null;
  }
}

export function IsHidden(props) {
  if (props.thread.is_hidden) {
    return <li className="thread-hidden">
      <span className="material-icon">
        visibility_off
      </span>
      <span className="icon-legend">
        {gettext("Hidden")}
      </span>
    </li>;
  } else {
    return null;
  }
}

export function IsClosed(props) {
  if (props.thread.is_closed) {
    return <li className="thread-closed">
      <span className="material-icon">
        lock_outline
      </span>
      <span className="icon-legend">
        {gettext("Closed")}
      </span>
    </li>;
  } else {
    return null;
  }
}

export function Replies(props) {
  const message = ngettext("%(replies)s reply", "%(replies)s replies", props.thread.replies);
  const legend = interpolate(message, {'replies': props.thread.replies}, true);

  return <li className="thread-replies">
    <span className="material-icon">
      forum
    </span>
    <span className="icon-legend">
      {legend}
    </span>
  </li>;
}

export function LastReply(props) {
  const date = interpolate(LAST_REPLY_URL, {
    absolute: escapeHtml(props.thread.last_post_on.format('LLL')),
    relative: escapeHtml(props.thread.last_post_on.fromNow())
  }, true);

  let user = null;
  if (props.thread.url.last_poster) {
    user = interpolate(LAST_POSTER_URL, {
      url: escapeHtml(props.thread.url.last_poster),
      user: escapeHtml(props.thread.last_poster_name)
    }, true);
  } else {
    user = interpolate(LAST_POSTER_SPAN, {
      user: escapeHtml(props.thread.last_poster_name)
    }, true);
  };

  const message = interpolate(escapeHtml(gettext("last reply by %(user)s %(date)s")), {
        date,
        user
  }, true);

  return <li className="thread-last-reply" dangerouslySetInnerHTML={{__html: message}}/>;
}

export default function(props) {
  return <div className="header-stats">
    <div className="container">
      <ul className="list-inline">
        <Weight thread={props.thread} />
        <Unapproved thread={props.thread} />
        <IsHidden thread={props.thread} />
        <IsClosed thread={props.thread} />
        <Replies thread={props.thread} />
        <LastReply thread={props.thread} />
      </ul>
    </div>
  </div>;
}
/* jshint ignore:end */