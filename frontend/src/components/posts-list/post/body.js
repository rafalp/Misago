/* jshint ignore:start */
import React from 'react';
import escapeHtml from 'misago/utils/escape-html';

const HIDDEN_BY_URL = '<a href="%(url)s" class="item-title">%(user)s</a>';
const HIDDEN_BY_SPAN = '<span class="item-title">%(user)s</span>';
const HIDDEN_ON = '<abbr class="last-title" title="%(absolute)s">%(relative)s</abbr>';

export default function(props) {
  if (props.post.is_hidden && !props.post.acl_can_see_hidden) {
    return <Hidden {...props} />;
  } else if (props.post.parsed) {
    return <Default {...props} />;
  } else {
    return <Invalid {...props} />;
  }
}

export function Default(props) {
 return (
    <div className="panel-body">
      <article className="misago-markup" dangerouslySetInnerHTML={{__html: props.post.parsed}} />
    </div>
  );
}

export function Hidden(props) {
  let user = null;
  if (props.post.hidden_by) {
    user = interpolate(HIDDEN_BY_URL, {
      url: escapeHtml(props.post.url.hidden_by),
      user: escapeHtml(props.post.hidden_by_name)
    }, true);
  } else {
    user = interpolate(HIDDEN_BY_SPAN, {
      user: escapeHtml(props.post.hidden_by_name)
    }, true);
  }

  const date = interpolate(HIDDEN_ON, {
    absolute: escapeHtml(props.post.hidden_on.format('LLL')),
    relative: escapeHtml(props.post.hidden_on.fromNow())
  }, true);

  const message = interpolate(escapeHtml(gettext("Hidden by %(hidden_by)s %(hidden_on)s.")), {
    hidden_by: user,
    hidden_on: date
  }, true);

  return (
    <div className="panel-body panel-body-hidden">
      <p className="lead">{gettext("This post is hidden. You cannot not see its contents.")}</p>
      <p className="text-muted" dangerouslySetInnerHTML={{__html: message}} />
    </div>
  );
}

export function Invalid(props) {
 return (
    <div className="panel-body panel-body-invalid">
      <p className="lead">{gettext("This post's contents cannot be displayed.")}</p>
      <p className="text-muted">{gettext("This error is caused by invalid post content manipulation.")}</p>
    </div>
  );
}