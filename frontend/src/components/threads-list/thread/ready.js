/* jshint ignore:start */
import React from 'react';
import Avatar from 'misago/components/avatar';
import { BottomDetails, TopDetails } from './details';
import LastAction from './last-action';
import { Options } from './options';
import UserUrl from './user-url';

export default function(props) {
  const {
    activeCategory,
    categories,
    list,
    thread,

    isBusy,
    isSelected,
    showOptions,
  } = props;

  let category = null;
  if (activeCategory.id !== thread.category) {
    category = categories[thread.category];
  }

  const flavor = category || activeCategory;

  let className = 'thread-main col-xs-12';
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
    <li className={getClassName(thread.is_read, isBusy, isSelected, flavor)}>
      <TopDetails
        category={category}
        thread={thread}
      />
      <div className="row thread-row">
        <div className={className}>

          <div className="media">
            <div className="media-left hidden-xs">

              <UserUrl
                className="thread-starter-avatar"
                title={thread.starter_name}
                url={thread.url.starter}
              >
                <Avatar
                  size={40}
                  user={thread.starter}
                />
              </UserUrl>

            </div>
            <div className="media-body">

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
          </div>

        </div>
        <div className="col-md-3 hidden-xs hidden-sm thread-last-action">
          <LastAction thread={thread} />
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

export function getClassName(isRead, isBusy, isSelected, flavor) {
  let styles = ['list-group-item'];

  if (flavor && flavor.css_class) {
    styles.push('list-group-category-has-flavor');
    styles.push('list-group-item-category-' + flavor.css_class);
  }

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