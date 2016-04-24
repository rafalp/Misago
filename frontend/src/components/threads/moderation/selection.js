import React from 'react';
import * as select from 'misago/reducers/selection'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line

export default class extends React.Component {
  /* jshint ignore:start */
  selectAll = () => {
    store.dispatch(select.all(this.props.threads.map(function(thread) {
      return thread.id;
    })));
  };

  selectNone = () => {
    store.dispatch(select.none());
  };
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    return <ul className={this.props.className}>
      <li>
        <button className="btn btn-link"
                type="button"
                onClick={this.selectAll}>
          <span className="material-icon">check_box</span>
          {gettext("Select all")}
        </button>
      </li>
      <li>
        <button className="btn btn-link"
                type="button"
                onClick={this.selectNone}>
          <span className="material-icon">check_box_outline_blank</span>
          {gettext("Select none")}
        </button>
      </li>
    </ul>;
    /* jshint ignore:end */
  }
}