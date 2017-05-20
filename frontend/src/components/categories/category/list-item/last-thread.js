// jshint ignore:start
import React from 'react';
import Avatar from 'misago/components/avatar';

export default function({ category }) {
  return (
    <div className="col-xs-12 col-sm-6 col-md-4 category-last-thread">
      <LastThread category={category} />
      <Empty category={category} />
      <Private category={category} />
      <Protected category={category} />
    </div>
  );
}

export function LastThread({ category }) {
  if (!category.acl.can_browse) return null;
  if (!category.acl.can_see_all_threads) return null;
  if (!category.last_thread_title) return null;

  return (
    <div className="media">
      <div className="media-left hidden-xs">
        <LastPosterAvatar category={category} />
      </div>
      <div className="media-body">
        <div className="media-heading">
          <a
            className="item-title thread-title"
            href={category.url.last_thread_new}
            title={category.last_thread_title}
          >
            {category.last_thread_title}
          </a>
        </div>
        <ul className="list-inline">
          <li className="category-last-thread-poster">
            <LastPosterName category={category} />
          </li>
          <li className="divider">
            &#8212;
          </li>
          <li className="category-last-thread-date">
            <a href={category.url.last_post}>
              {category.last_post_on.fromNow()}
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
}

export function LastPosterAvatar({ category }) {
  if (category.last_poster) {
    return (
      <a
        className="last-poster-avatar"
        href={category.last_poster.url}
        title={category.last_poster_name}
      >
        <Avatar
          className="media-object"
          size={40}
          user={category.last_poster}
        />
      </a>
    );
  }

  return (
      <span
        className="last-poster-avatar"
        title={category.last_poster_name}
      >
        <Avatar
          className="media-object"
          size={40}
        />
      </span>
  );
}

export function LastPosterName({ category }) {
  if (category.last_poster) {
    return (
      <a
        className="item-title"
        href={category.last_poster.url}
      >
        {category.last_poster_name}
      </a>
    );
  }

  return (
    <span className="item-title">
      {category.last_poster_name}
    </span>
  );
}

export function Empty({ category }) {
  if (!category.acl.can_browse) return null;
  if (!category.acl.can_see_all_threads) return null;
  if (category.last_thread_title) return null;

  return (
    <Message
      message={gettext("This category is empty. No threads were posted within it so far.")}
    />
  );
}

export function Private({ category }) {
  if (!category.acl.can_browse) return null;
  if (category.acl.can_see_all_threads) return null;

  return (
    <Message
      message={gettext("This category is private. You can see only your own threads within it.")}
    />
  );
}

export function Protected({ category }) {
  if (category.acl.can_browse) return null;

  return (
    <Message
      message={gettext("This category is protected. You can't browse it's contents.")}
    />
  );
}

export function Message({ message }) {
  return (
    <div className="media category-thread-message">
      <div className="media-left">
        <span className="material-icon">
          info_outline
        </span>
      </div>
      <div className="media-body">
        <p>
          {message}
        </p>
      </div>
    </div>
  );
}