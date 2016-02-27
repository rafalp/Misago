import React from 'react';

export default class extends React.Component {
  getThreadsCount() {
    let string = ngettext(
      "%(threads)s thread",
      "%(threads)s threads",
      this.props.category.threads);

    return interpolate(string, {
      'threads': this.props.category.threads
    }, true);
  }

  getPostsCount() {
    let string = ngettext(
      "%(posts)s post",
      "%(posts)s posts",
      this.props.category.posts);

    return interpolate(string, {
      'posts': this.props.category.posts
    }, true);
  }

  render() {
    /* jshint ignore:start */
    return <ul className="list-inline category-stats">
      <li className="category-threads">
        {this.getThreadsCount()}
      </li>
      <li className="category-posts">
        {this.getPostsCount()}
      </li>
    </ul>;
    /* jshint ignore:end */
  }
}