/* jshint ignore:start */
import React from 'react';
import escapeHtml from 'misago/utils/escape-html';

const MESSAGE = {
  pinned_globally: gettext("Thread has been pinned globally."),
  pinned_locally: gettext("Thread has been pinned locally."),
  unpinned: gettext("Thread has been unpinned."),

  approved: gettext("Thread has been approved."),

  opened: gettext("Thread has been opened."),
  closed: gettext("Thread has been closed."),

  unhid: gettext("Thread has been revealed."),
  hid: gettext("Thread has been made hidden."),
}

const FROM_CATEGORY = '<a href="%(url)s" class="item-title">%(name)s</a>'
const OLD_TITLE = '<span class="item-title">%(old_title)s</span>';
const MERGED_THREAD = '<span class="item-title">%(merged_thread)s</span>';

export default function(props) {
  if (MESSAGE[props.post.event_type]) {
    return (
      <p className="event-message">
        {MESSAGE[props.post.event_type]}
      </p>
    );
  } else if (props.post.event_type === 'changed_title') {
    return (
      <ChangedTitle {...props} />
    );
  } else if (props.post.event_type === 'moved') {
    return (
      <Moved {...props} />
    );
  } else if (props.post.event_type === 'merged') {
    return (
      <Merged {...props} />
    );
  } else {
    return null;
  }
}

export function ChangedTitle(props) {
  const msgstring = escapeHtml(gettext("Thread title has been changed from %(old_title)s."));
  const oldTitle = interpolate(OLD_TITLE, {
    old_title: escapeHtml(props.post.event_context.old_title)
  }, true);

  const message = interpolate(msgstring, {
    old_title: oldTitle
  }, true);

  return (
    <p className="event-message" dangerouslySetInnerHTML={{__html: message}} />
  );
}

export function Moved(props) {
  const msgstring = escapeHtml(gettext("Thread has been moved from %(from_category)s."));
  const fromCategory = interpolate(FROM_CATEGORY, {
    url: escapeHtml(props.post.event_context.from_category.url),
    name: escapeHtml(props.post.event_context.from_category.name)
  }, true);

  const message = interpolate(msgstring, {
    from_category: fromCategory
  }, true);

  return (
    <p className="event-message" dangerouslySetInnerHTML={{__html: message}} />
  );
}

export function Merged(props) {
  const msgstring = escapeHtml(gettext("The %(merged_thread)s thread has been merged into this thread."));
  const mergedThread = interpolate(MERGED_THREAD, {
    merged_thread: escapeHtml(props.post.event_context.merged_thread)
  }, true);

  const message = interpolate(msgstring, {
    merged_thread: mergedThread
  }, true);

  return (
    <p className="event-message" dangerouslySetInnerHTML={{__html: message}} />
  );
}