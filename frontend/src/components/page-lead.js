import React from 'react';
import stringCount from 'misago/utils/string-count';

export default class extends React.Component {
  getClassName() {
    let className = 'page-lead';

    if (this.props.className) {
      className += ' ' + this.props.className;
    }

    if (this.props.copy && this.props.copy.length) {
      if (stringCount(this.props.copy, '<p') === 1 && this.props.copy.indexOf('<br') === -1) {
        className += ' lead';
      }
    }

    return className;
  }

  render() {
    if (this.props.copy && this.props.copy.length) {
      /* jshint ignore:start */
      return <div className={this.getClassName()} dangerouslySetInnerHTML={{
        __html: this.props.copy
      }} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }
}