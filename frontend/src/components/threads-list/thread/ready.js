/* jshint ignore:start */
import React from 'react';
import { BottomDetails, TopDetails } from './details';
import { Options } from './options';

export default function(props) {
  const {
    categories,
    list,
    thread,

    isBusy,
    isSelected,
    showOptions,
  } = props;

  const category = categories[thread.category];

  let className = 'col-xs-12';
  if (showOptions) {
    if (thread.moderation.length) {
      className += ' col-sm-9 col-md-7';
    } else {
      className += ' col-sm-10 col-md-7';
    }
  } else {
    className += ' col-sm-12 col-md-9';
  }

  return (
    <li className={getClassName(thread.is_read, isBusy, isSelected)}>
      <div className="row">
        <div className={className}>

          <TopDetails
            category={category}
            thread={thread}
          />

          <a href={thread.url.index} className="item-title thread-title">
            {thread.title}
          </a>

          <BottomDetails
            category={category}
            disabled={isBusy}
            isSelected={isSelected}
            showOptions={showOptions}
            thread={thread}
          />

        </div>
        <div className="col-md-3 hidden-xs hidden-sm thread-last-action">
          <div className="row">
            <div className="col-xs-5">
              <Timestamp
                datetime={thread.last_post_on}
                url={thread.url.last_post}
              />
            </div>
            <div className="col-xs-7">
              <LastPoster
                posterName={thread.last_poster_name}
                url={thread.url.last_poster}
              />
            </div>
          </div>
        </div>
        <Options
          disabled={isBusy}
          display={showOptions}
          isSelected={isSelected}
          thread={thread}
        />
      </div>
    </li>
  );
}

export function getClassName(isRead, isBusy, isSelected) {
  let styles = ['list-group-item'];

  if (isRead) {
    styles.push('thread-read');
  } else {
    styles.push('thread-new');
  }

  if (isBusy) {
    styles.push('thread-busy');
  } else if (isSelected) {
    styles.push('thread-selected');
  }

  return styles.join(' ');
}

export function Timestamp({ datetime, url }) {
  return (
    <a href={url} title={datetime.format('LLL')}>
      {datetime.fromNow(true)}
    </a>
  );
}

export function LastPoster(props) {
  const { posterName, url } = props;

  if (url) {
    return (
      <a
        className="item-title thread-last-poster"
        href={url}
      >
        {posterName}
      </a>
    );
  }

  return (
    <span className="item-title thread-last-poster">
      {posterName}
    </span>
  );
}