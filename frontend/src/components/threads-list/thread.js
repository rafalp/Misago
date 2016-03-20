import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import ReadIcon from 'misago/components/threads-list/read-icon'; // jshint ignore:line
import escapeHtml from 'misago/utils/escape-html';

const LAST_POSTER_URL = '<a href="%(url)s" class="item-title">%(user)s</a>';
const LAST_POSTER_SPAN = '<span class="item-title">%(user)s</span>';
const LAST_REPLY_URL = '<a href="%(url)s" class="goto-last" title="%(absolute)s">%(relative)s</a>';

export class Category extends React.Component {
  getClassName() {
    if (this.props.category.css_class) {
      return 'thread-category thread-category-' + this.props.category.css_class;
    } else {
      return 'thread-category';
    }
  }

  getUrl() {
    return this.props.category.absolute_url + this.props.list.path;
  }

  render() {
    /* jshint ignore:start */
    return <Link to={this.getUrl()} className={this.getClassName()}>
      {this.props.category.name}
    </Link>;
    /* jshint ignore:end */
  }
}

export default class extends React.Component {
  getPath() {
    let top = this.props.categories[this.props.thread.top_category];
    let bottom = this.props.categories[this.props.thread.category];

    if (top && bottom && top.id !== bottom.id) {
      /* jshint ignore:start */
      return <li className="thread-path">
        <Category category={top} list={this.props.list} />
        <span className="path-separator material-icon">
          chevron_right
        </span>
        <Category category={bottom} list={this.props.list} />
      </li>;
      /* jshint ignore:end */
    } else if (top || bottom) {
      /* jshint ignore:start */
      return <li className="thread-path">
        <Category category={top || bottom} list={this.props.list} />
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
        {gettext("Closed")}
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getNewLabel() {
    if (!this.props.thread.is_read) {
      /* jshint ignore:start */
      return <li className="thread-new-posts"
                 title={gettext("Go to first unread post")}>
        <a href={this.props.thread.new_post_url}>
          {gettext("New posts")}
        </a>
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
      <a href={this.props.thread.absolute_url}>
        {interpolate(message, {
          replies: this.props.thread.replies,
        }, true)}
      </a>
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
      escapeHtml(gettext("last reply %(date)s by %(user)s")), {
        date: this.getLastReplyDate(),
        user: this.getLastPoster()
      }, true)}} />;
    /* jshint ignore:end */
  }

  getClassName() {
    if (this.props.thread.is_read) {
      return 'list-group-item thread-read';
    } else {
      return 'list-group-item thread-new';
    }
  }

  render () {
    /* jshint ignore:start */
    return <li className={this.getClassName()}>

      <ReadIcon thread={this.props.thread} />
      <div className="thread-main">

        <a href={this.props.thread.absolute_url} className="item-title thread-title">
          {this.props.thread.title}
        </a>

        <ul className="list-inline">
          {this.getPath()}
          {this.getClosedLabel()}
          {this.getNewLabel()}
          {this.getRepliesCount()}
          {this.getLastReply()}
        </ul>
      </div>

    </li>;
    /* jshint ignore:end */
  }
}