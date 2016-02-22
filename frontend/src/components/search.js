import React from 'react';

export default class extends React.Component {
  getClassName() {
    if (this.props.className) {
      return "form-search " + this.props.className;
    } else {
      return "form-search";
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <input type="text"
             className="form-control"
             value={this.props.value}
             onChange={this.props.onChange}
             placeholder={this.props.placeholder || gettext("Search...")} />
      <span className="material-icon">
        search
      </span>
    </div>;
    /* jshint ignore:end */
  }
}