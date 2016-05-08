import React from 'react';
import Category from 'misago/components/threads-list/thread/category'; // jshint ignore:line
import escapeHtml from 'misago/utils/escape-html';

const LAST_POSTER_URL = '<a href="%(url)s" class="poster-title">%(user)s</a>';
const LAST_POSTER_SPAN = '<span class="poster-title">%(user)s</span>';
const LAST_REPLY_URL = '<a href="%(url)s" class="last-title" title="%(absolute)s">%(relative)s</a>';

export default class extends React.Component {
  getNewLabel() {
    if (!this.props.thread.is_read) {
      /* jshint ignore:start */
      return <li className="thread-new-posts"
                 title={gettext("Go to first unread post")}>
        <a href={this.props.thread.new_post_url}>
          <span className="material-icon">
            comment
          </span>
          <span className="icon-legend">
            {gettext("New posts")}
          </span>
        </a>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getPinnedLabel() {
    if (this.props.thread.weight === 2) {
      /* jshint ignore:start */
      return <li className="thread-pinned-globally">
        <span className="material-icon">
          bookmark_border
        </span>
        <span className="icon-legend">
          {gettext("Pinned globally")}
        </span>
      </li>;
      /* jshint ignore:end */
    } else if (this.props.thread.weight === 1) {
      /* jshint ignore:start */
      return <li className="thread-pinned-locally">
        <span className="material-icon">
          bookmark_border
        </span>
        <span className="icon-legend">
          {gettext("Pinned locally")}
        </span>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getUnapprovedLabel() {
    if (this.props.thread.is_unapproved) {
      /* jshint ignore:start */
      return <li className="thread-unapproved">
        <span className="material-icon">
          remove_circle
        </span>
        <span className="icon-legend">
          {gettext("Unapproved")}
        </span>
      </li>;
      /* jshint ignore:end */
    } else if (this.props.thread.has_unapproved_posts) {
      /* jshint ignore:start */
      return <li className="thread-unapproved-posts">
        <span className="material-icon">
          remove_circle_outline
        </span>
        <span className="icon-legend">
          {gettext("Unapproved posts")}
        </span>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getHiddenLabel() {
    if (this.props.thread.is_hidden) {
      /* jshint ignore:start */
      return <li className="thread-hidden">
        <span className="material-icon">
          visibility_off
        </span>
        <span className="icon-legend">
          {gettext("Hidden")}
        </span>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getClosedLabel() {
    if (this.props.thread.is_closed) {
      /* jshint ignore:start */
      return <li className="thread-closed">
        <span className="material-icon">
          lock_outline
        </span>
        <span className="icon-legend">
          {gettext("Closed")}
        </span>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getPath() {
    let top = this.props.categories[this.props.thread.top_category];
    let bottom = this.props.categories[this.props.thread.category];

    if (top && bottom && top.id !== bottom.id) {
      /* jshint ignore:start */
      return <li className="thread-path">
        <Category category={top} list={this.props.list} />
        <span className="path-separator material-icon">
          arrow_forward
        </span>
        <Category category={bottom} list={this.props.list} />
      </li>;
      /* jshint ignore:end */
    } else if (top) {
      /* jshint ignore:start */
      return <li className="thread-path">
        <Category category={top} list={this.props.list} />
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getRepliesCount() {
    /* jshint ignore:start */
    let message = ngettext(
        "%(replies)s reply",
        "%(replies)s replies",
        this.props.thread.replies);

    return <li className="thread-replies">
      <span className="material-icon">
        forum
      </span>
      <span className="icon-legend">
        {interpolate(message, {
          replies: this.props.thread.replies,
        }, true)}
      </span>
    </li>;
    /* jshint ignore:end */
  }

  getLastReplyDate() {
    return interpolate(LAST_REPLY_URL, {
      url: escapeHtml(this.props.thread.last_post_url),
      absolute: escapeHtml(this.props.thread.last_post_on.format('LLL')),
      relative: escapeHtml(this.props.thread.last_post_on.fromNow())
    }, true);
  }

  getLastPoster() {
    if (this.props.thread.last_poster_url) {
      return interpolate(LAST_POSTER_URL, {
        url: escapeHtml(this.props.thread.last_poster_url),
        user: escapeHtml(this.props.thread.last_poster_name)
      }, true);
    } else {
      return interpolate(LAST_POSTER_SPAN, {
        user: escapeHtml(this.props.thread.last_poster_name)
      }, true);
    }
  }

  getLastReply() {
    /* jshint ignore:start */
    return <li className="thread-last-reply"
               dangerouslySetInnerHTML={{__html: interpolate(
      escapeHtml(gettext("last reply by %(user)s %(date)s")), {
        date: this.getLastReplyDate(),
        user: this.getLastPoster()
      }, true)}} />;
    /* jshint ignore:end */
  }

  render () {
    /* jshint ignore:start */
    return <ul className="thread-details-full list-inline">
      {this.getNewLabel()}
      {this.getPinnedLabel()}
      {this.getUnapprovedLabel()}
      {this.getHiddenLabel()}
      {this.getClosedLabel()}
      {this.getPath()}
      {this.getRepliesCount()}
      {this.getLastReply()}
    </ul>;
    /* jshint ignore:end */
  }
}