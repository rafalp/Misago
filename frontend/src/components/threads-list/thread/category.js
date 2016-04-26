import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line

export default class extends React.Component {
  getUrl() {
    return this.props.category.absolute_url + this.props.list.path;
  }

  getClassName() {
    if (this.props.category.css_class) {
      return 'thread-category thread-category-' + this.props.category.css_class;
    } else {
      return 'thread-category';
    }
  }

  render() {
    /* jshint ignore:start */
    return <Link to={this.getUrl()} className={this.getClassName()}>
      {this.props.category.name}
    </Link>;
    /* jshint ignore:end */
  }
}