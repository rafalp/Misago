import React from 'react';
import * as random from 'misago/utils/random'; // jshint ignore:line

export default class extends React.Component {
  shouldComponentUpdate() {
    return false;
  }

  getClassName() {
    if (this.props.hiddenOnMobile) {
      return 'list-group-item thread-preview hidden-xs hidden-sm';
    } else {
      return 'list-group-item thread-preview';
    }
  }

  render () {
    /* jshint ignore:start */
    return <li className={this.getClassName()}>
      <div className="thread-icon">
        <span className="read-status item-read">
          <span className="material-icon">
            chat_bubble_outline
          </span>
        </span>
      </div>

      <div className="thread-main">

        <span className="item-title thread-title">
          <span className="ui-preview-text"
              style={{width: random.int(60, 200) + "px"}}>
            &nbsp;
          </span>
        </span>

        <ul className="thread-details-compact list-inline">
          <li>
            <span className="ui-preview-text"
                style={{width: random.int(20, 70) + "px"}}>
              &nbsp;
            </span>
          </li>
          <li>
            <span className="ui-preview-text"
                style={{width: random.int(20, 70) + "px"}}>
              &nbsp;
            </span>
          </li>
          <li>
            <span className="ui-preview-text"
                style={{width: random.int(20, 70) + "px"}}>
              &nbsp;
            </span>
          </li>
        </ul>

        <ul className="thread-details-full list-inline">
          <li>
            <span className="ui-preview-text"
                style={{width: random.int(50, 150) + "px"}}>
              &nbsp;
            </span>
          </li>
          <li>
            <span className="ui-preview-text"
                style={{width: random.int(50, 100) + "px"}}>
              &nbsp;
            </span>
          </li>
          <li>
            <span className="ui-preview-text"
                style={{width: random.int(100, 250) + "px"}}>
              &nbsp;
            </span>
          </li>
        </ul>

      </div>

      <div className="clearfix" />
    </li>;
    /* jshint ignore:end */
  }
}