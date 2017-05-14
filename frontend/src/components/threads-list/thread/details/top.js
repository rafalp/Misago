/* jshint ignore:start */
import React from 'react';
import Category from './category';

export default function({ category, thread }) {
  return (
    <div className="thread-details-top">
      <NewLabel
        isRead={thread.is_read}
        url={thread.url.new_post}
      />
      <PinnedLabel weight={thread.weight} />
      <UnapprovedLabel
        thread={thread.is_unapproved}
        posts={thread.has_unapproved_posts}
      />
      <Category
        className="item-title thread-detail-category visible-xs-inline-block"
        category={category}
      />
      <LastReplyLabel
        datetime={thread.last_post_on}
        url={thread.url.last_post}
      />
      <LastPoster
        posterName={thread.last_poster_name}
        url={thread.url.last_poster}
      />
    </div>
  );
}

export function NewLabel({ isRead, url }) {
  if (isRead) return null;

  return (
    <a
      className="thread-detail-new"
      href={url}
    >
      <span className="material-icon">
        comment
      </span>
      <span className="detail-text">
        {gettext("New posts")}
      </span>
    </a>
  )
}

export function PinnedLabel({ weight }) {
  if (weight === 0) return null;

  let className = 'thread-detail-pinned-globally'
  let icon = 'bookmark';
  let text = gettext("Pinned globally");

  if (weight === 1) {
    className = 'thread-detail-pinned-locally'
    icon = 'bookmark_border';
    text = gettext("Pinned locally");
  }

  return (
    <span className={className}>
      <span className="material-icon">
        {icon}
      </span>
      <span className="detail-text">
        {text}
      </span>
    </span>
  )
}

export function UnapprovedLabel({ posts, thread }) {
  if (!posts && !thread) return null;

  let className = 'thread-detail-unapproved-posts'
  let icon = 'remove_circle_outline';
  let text = gettext("Unapproved posts");

  if (thread) {
    className = 'thread-detail-unapproved'
    icon = 'remove_circle';
    text = gettext("Unapproved");
  }

  return (
    <span className={className}>
      <span className="material-icon">
        {icon}
      </span>
      <span className="detail-text">
        {text}
      </span>
    </span>
  )
}

export function LastReplyLabel({ datetime, url }) {
  return (
    <a
      className="visible-xs-inline-block thread-detail-last-reply"
      href={url}
      title={datetime.format('LLL')}
    >
      {datetime.fromNow(true)}
    </a>
  )
}

export function LastPoster(props) {
  const { posterName, url } = props;

  if (url) {
    return (
      <a
        className="visible-xs-inline-block item-title thread-last-poster"
        href={url}
      >
        {posterName}
      </a>
    );
  }

  return (
    <span className="visible-xs-inline-block item-title thread-last-poster">
      {posterName}
    </span>
  );
}