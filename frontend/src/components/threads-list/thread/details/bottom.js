/* jshint ignore:start */
import React from 'react';
import { OptionsXs } from '../options';

export default function({category, isBusy, showOptions, isSelected, thread}) {
  let className = 'col-xs-12 col-sm-12';
  if (showOptions) {
    if (thread.moderation.length) {
      className = 'col-xs-6 col-sm-12';
    } else {
      className = 'col-xs-9 col-sm-12';
    }
  }

  let statusFlags = 0;
  if (thread.is_hidden) statusFlags += 1;
  if (thread.is_closed) statusFlags += 1;
  if (thread.has_poll) statusFlags += 1;

  let allFlagsVisible = showOptions && statusFlags === 3;

  let textClassName = 'detail-text hidden-xs';
  if (allFlagsVisible) {
    textClassName += ' hidden-sm'
  }

  return (
    <div className="row thread-details-bottom">
      <div className={className}>
        <a
          className="item-title thread-detail-category hidden-xs"
          href={category.absolute_url}
        >
          {category.name}
        </a>
        <HiddenLabel
          textClassName={textClassName}
          display={thread.is_hidden}
        />
        <ClosedLabel
          textClassName={textClassName}
          display={thread.is_closed}
        />
        <PollLabel
          textClassName={textClassName}
          display={thread.has_poll}
        />
        <RepliesLabel
          forceFullText={!showOptions || statusFlags < 2}
          replies={thread.replies}
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
      <OptionsXs
        disabled={isBusy}
        display={showOptions}
        isSelected={isSelected}
        thread={thread}
      />
    </div>
  );
}

export function HiddenLabel({ display, textClassName }) {
  if (!display) return null;

  return (
    <span className="thread-detail-hidden">
      <span className="material-icon">
        visibility_off
      </span>
      <span className={textClassName}>
        {gettext("Hidden")}
      </span>
    </span>
  )
}

export function ClosedLabel({ display, textClassName }) {
  if (!display) return null;

  return (
    <span className="thread-detail-closed">
      <span className="material-icon">
        lock_outline
      </span>
      <span className={textClassName}>
        {gettext("Closed")}
      </span>
    </span>
  )
}

export function PollLabel({ display, textClassName }) {
  if (!display) return null;

  return (
    <span className="thread-detail-poll">
      <span className="material-icon">
        assessment
      </span>
      <span className={textClassName}>
        {gettext("Poll")}
      </span>
    </span>
  )
}

export function RepliesLabel({ replies, forceFullText }) {
  const text = ngettext(
    "%(replies)s reply",
    "%(replies)s replies",
    replies);

  let compactClassName = '';
  let fullClassName = '';

  if (forceFullText) {
    compactClassName = 'detail-text hide';
    fullClassName = 'detail-text';
  } else {
    compactClassName = 'detail-text visible-xs-inline-block';
    fullClassName = 'detail-text hidden-xs';
  }

  return (
    <span className="thread-detail-replies">
      <span className="material-icon">
        forum
      </span>
      <span className={compactClassName}>
        {replies}
      </span>
      <span className={fullClassName}>
        {interpolate(text, { replies }, true)}
      </span>
    </span>
  )
}

export function LastReplyLabel({ datetime, url }) {
  return (
    <a
      className="visible-sm-inline-block thread-detail-last-reply"
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
        className="visible-sm-inline-block item-title thread-last-poster"
        href={url}
      >
        {posterName}
      </a>
    );
  }

  return (
    <span className="visible-sm-inline-block item-title thread-last-poster">
      {posterName}
    </span>
  );
}