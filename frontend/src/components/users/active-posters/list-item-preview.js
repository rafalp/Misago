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
        <div className="rank-user-avatar">
          <span>
            <Avatar size="50" />
          </span>
        </div>

        <div className="rank-user">
          <div className="user-name">
            <span className="item-title">
              <span
                className="ui-preview-text"
                style={{ width: random.int(30, 80) + "px" }}
              >
                &nbsp;
              </span>
            </span>
          </div>

          <div className="user-details">
            <span className="user-status">
              <span className="status-icon ui-preview-text">&nbsp;</span>
              <span
                className="status-label ui-preview-text hidden-xs hidden-sm"
                style={{ width: random.int(30, 50) + "px" }}
              >
                &nbsp;
              </span>
            </span>
            <span className="rank-name">
              <span
                className="ui-preview-text"
                style={{ width: random.int(30, 50) + "px" }}
              >
                &nbsp;
              </span>
            </span>
            <span className="user-title hidden-xs hidden-sm">
              <span
                className="ui-preview-text"
                style={{ width: random.int(30, 50) + "px" }}
              >
                &nbsp;
              </span>
            </span>
          </div>
          <div className="user-compact-stats visible-xs-block">
            <span className="rank-position">
              <strong>
                <span
                  className="ui-preview-text"
                  style={{ width: random.int(20, 30) + "px" }}
                >
                  &nbsp;
                </span>
              </strong>
              <small>{pgettext("top posters list item", "Rank")}</small>
            </span>
            <span className="rank-posts-counted">
              <strong>
                <span
                  className="ui-preview-text"
                  style={{ width: random.int(20, 30) + "px" }}
                >
                  &nbsp;
                </span>
              </strong>
              <small>{pgettext("top posters list item", "Ranked posts")}</small>
            </span>
          </div>
        </div>

        <div className="rank-position hidden-xs">
          <strong>
            <span
              className="ui-preview-text"
              style={{ width: random.int(20, 30) + "px" }}
            >
              &nbsp;
            </span>
          </strong>
          <small>{pgettext("top posters list item", "Rank")}</small>
        </div>

        <div className="rank-posts-counted hidden-xs">
          <strong>
            <span
              className="ui-preview-text"
              style={{ width: random.int(20, 30) + "px" }}
            >
              &nbsp;
            </span>
          </strong>
          <small>{pgettext("top posters list item", "Ranked posts")}</small>
        </div>

        <div className="rank-posts-total hidden-xs">
          <strong>
            <span
              className="ui-preview-text"
              style={{ width: random.int(20, 30) + "px" }}
            >
              &nbsp;
            </span>
          </strong>
          <small>{pgettext("top posters list item", "Total posts")}</small>
        </div>
      </li>
    )
  }
}
