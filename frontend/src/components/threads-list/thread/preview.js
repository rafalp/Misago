import React from "react"
import * as random from "misago/utils/random"

export default class extends React.Component {
  shouldComponentUpdate() {
    return false
  }

  render() {
    return (
      <li className="list-group-item thread-preview">
        <div className="thread-details-top visible-xs-block">
          <span
            className="ui-preview-text"
            style={{ width: random.int(30, 80) + "px" }}
          >
            &nbsp;
          </span>
          <span
            className="ui-preview-text"
            style={{ width: random.int(30, 80) + "px" }}
          >
            &nbsp;
          </span>
          <span
            className="ui-preview-text"
            style={{ width: random.int(30, 80) + "px" }}
          >
            &nbsp;
          </span>
        </div>

        <span className="item-title thread-title">
          <span
            className="ui-preview-text"
            style={{ width: random.int(60, 200) + "px" }}
          >
            &nbsp;
          </span>
          <span
            className="ui-preview-text hidden-xs"
            style={{ width: random.int(60, 200) + "px" }}
          >
            &nbsp;
          </span>
          <span
            className="ui-preview-text hidden-xs"
            style={{ width: random.int(60, 200) + "px" }}
          >
            &nbsp;
          </span>
        </span>

        <div className="thread-details-bottom">
          <div>
            <span
              className="ui-preview-text"
              style={{ width: random.int(30, 80) + "px" }}
            >
              &nbsp;
            </span>
            <span
              className="ui-preview-text"
              style={{ width: random.int(30, 80) + "px" }}
            >
              &nbsp;
            </span>
            <span
              className="ui-preview-text"
              style={{ width: random.int(30, 80) + "px" }}
            >
              &nbsp;
            </span>
          </div>
        </div>
      </li>
    )
  }
}
