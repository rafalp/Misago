import React from 'react';

export default class extends React.Component {
  getLastPoster() {
    if (this.props.category.last_poster_url) {
      /* jshint ignore:start */
      return <a href={this.props.category.last_poster_url}
                className="item-title">
        {this.props.category.last_poster_name}
      </a>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <span className="item-title">
        {this.props.category.last_poster_name}
      </span>;
      /* jshint ignore:end */
    }
  }

  getThreadDetails() {
    /* jshint ignore:start */
    return [
      <li className="thread-title" key="title">
        <a href={this.props.category.last_thread_url} className="item-title">
          {this.props.category.last_thread_title}
        </a>
      </li>,
      <li className="poster-name" key="poster">
        {this.getLastPoster()}
      </li>,
      <li className="thread-date" key="date">
        <abbr title={this.props.category.last_post_on.format('LL, LT')}>
          {this.props.category.last_post_on.fromNow()}
        </abbr>
      </li>
    ];
    /* jshint ignore:end */
  }

  getLastActivity() {
    if (this.props.category.acl.can_browse) {
      if (!this.props.category.acl.can_see_all_threads) {
        /* jshint ignore:start */
        return <li className="thread-message">
          <span className="material-icon">
            info_outline
          </span>
          {gettext("This category is private. You can see only your own threads within it.")}
        </li>;
        /* jshint ignore:end */
      } else if (this.props.category.last_thread_title) {
        return this.getThreadDetails();
      } else {
        /* jshint ignore:start */
        return <li className="thread-message">
          <span className="material-icon">
            error_outline
          </span>
          {gettext("This category is empty.")}
        </li>;
        /* jshint ignore:end */
      }
    } else {
      /* jshint ignore:start */
      return <li className="thread-message">
        <span className="material-icon">
          highlight_off
        </span>
        {gettext("This category is protected. You can't browse it's contents.")}
      </li>;
      /* jshint ignore:end */
    }
  }

  render() {
    /* jshint ignore:start */
    return <ul className="list-inline category-last-activity">
      {this.getLastActivity()}
    </ul>;
    /* jshint ignore:end */
  }
}