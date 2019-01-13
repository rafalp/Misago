import React from "react"
import Avatar from "misago/components/avatar"
import * as random from "misago/utils/random"

export default class extends React.Component {
  shouldComponentUpdate() {
    return false
  }

  getClassName() {
    if (this.props.hiddenOnMobile) {
      return "list-group-item hidden-xs hidden-sm"
    } else {
      return "list-group-item"
    }
  }

  render() {
    return (
      <li className={this.getClassName()}>
        <div className="change-avatar">
          <span className="user-avatar">
            <Avatar size="100" />
          </span>
        </div>
        <div className="change-author">
          <span
            className="ui-preview-text"
            style={{ width: random.int(30, 100) + "px" }}
          >
            &nbsp;
          </span>
        </div>
        <div className="change">
          <span
            className="ui-preview-text"
            style={{ width: random.int(30, 70) + "px" }}
          >
            &nbsp;
          </span>
          <span className="material-icon">arrow_forward</span>
          <span
            className="ui-preview-text"
            style={{ width: random.int(30, 70) + "px" }}
          >
            &nbsp;
          </span>
        </div>
        <div className="change-date">
          <span
            className="ui-preview-text"
            style={{ width: random.int(80, 140) + "px" }}
          >
            &nbsp;
          </span>
        </div>
      </li>
    )
  }
}
