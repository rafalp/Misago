import React from 'react';
import escapeHtml from 'misago/utils/escape-html';

const LAST_POSTER_URL = '<a href="%(url)s" class="poster-title">%(user)s</a>';
const LAST_POSTER_SPAN = '<span class="poster-title">%(user)s</span>';
const THREAD_URL = '<a href="%(url)s" class="item-title thread-title">%(thread)s</a>';
const LAST_POST_URL = '<a href="%(url)s" class="last-title" title="%(absolute)s">%(relative)s</a>';

export class LastPostMessage extends React.Component {
  getLastPoster() {
    if (this.props.category.last_poster_url) {
      return interpolate(LAST_POSTER_URL, {
        url: escapeHtml(this.props.category.last_poster_url),
        user: escapeHtml(this.props.category.last_poster_name)
      }, true);
    } else {
      return interpolate(LAST_POSTER_SPAN, {
        user: escapeHtml(this.props.category.last_poster_name)
      }, true);
    }
  }

  getLastThread() {
    return interpolate(THREAD_URL, {
      url: escapeHtml(this.props.category.last_thread_url),
      thread: escapeHtml(this.props.category.last_thread_title)
    }, true);
  }

  getLastReplyDate() {
    return interpolate(LAST_POST_URL, {
      url: escapeHtml(this.props.category.last_post_url),
      absolute: escapeHtml(this.props.category.last_post_on.format('LLL')),
      relative: escapeHtml(this.props.category.last_post_on.fromNow())
    }, true);
  }

  render() {
    /* jshint ignore:start */
    return <p className="category-last-post"
               dangerouslySetInnerHTML={{__html: interpolate(
      escapeHtml(gettext("Last post in %(thread)s by %(user)s %(date)s")), {
        thread: this.getLastThread(),
        date: this.getLastReplyDate(),
        user: this.getLastPoster()
      }, true)}} />;
    /* jshint ignore:end */
  }
}

export class EmptyMessage extends React.Component {
  render() {
    /* jshint ignore:start */
    return <p className="category-thread-message">
      <span className="material-icon">
        error_outline
      </span>
      {gettext("This category is empty.")}
    </p>;
    /* jshint ignore:end */
  }
}

export class PrivateMessage extends React.Component {
  render() {
    /* jshint ignore:start */
    return <p className="category-thread-message">
      <span className="material-icon">
        info_outline
      </span>
      {gettext("This category is private. You can see only your own threads within it.")}
    </p>;
    /* jshint ignore:end */
  }
}

export class ProtectedMessage extends React.Component {
  render() {
    /* jshint ignore:start */
    return <p className="category-thread-message">
      <span className="material-icon">
        highlight_off
      </span>
      {gettext("This category is protected. You can't browse it's contents.")}
    </p>;
    /* jshint ignore:end */
  }
}

export default class extends React.Component {
  render() {
    if (this.props.category.acl.can_browse) {
      if (!this.props.category.acl.can_see_all_threads) {
        /* jshint ignore:start */
        return <PrivateMessage />;
        /* jshint ignore:end */
      } else if (this.props.category.last_thread_title) {
        /* jshint ignore:start */
        return <LastPostMessage category={this.props.category} />;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <EmptyMessage />;
        /* jshint ignore:end */
      }
    } else {
      /* jshint ignore:start */
      return <ProtectedMessage />;
      /* jshint ignore:end */
    }
  }
}