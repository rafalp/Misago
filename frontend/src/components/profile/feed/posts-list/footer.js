// jshint ignore:start
import React from 'react';
import MisagoMarkup from 'misago/components/misago-markup';
import escapeHtml from 'misago/utils/escape-html';

const CATEGORY_SPAN = '<span class="category-name">%(name)s</span>';
const THREAD_SPAN = '<span class="item-title">%(title)s</span>';

export default function(props) {
  const template = gettext('%(posted_on)s in "%(thread)s", %(category)s');
  const message = interpolate(escapeHtml(template), {
    category: interpolate(CATEGORY_SPAN, {
      name: escapeHtml(props.category.name)
    }, true),
    thread: interpolate(THREAD_SPAN, {
      title: escapeHtml(props.thread.title)
    }, true),
    posted_on: escapeHtml(props.post.hidden_on.fromNow()),
  }, true);

  return (
    <div className="panel-footer post-infeed-footer">
      <a
        dangerouslySetInnerHTML={{__html: message}}
        href={props.post.url.index}
      />
    </div>
  );
}