import React from "react"
import Avatar from "misago/components/avatar"
import * as random from "misago/utils/random"

export default class extends React.Component {
  shouldComponentUpdate() {
    return false
  }

  render() {
    return (
      <div className="panel user-card user-card-preview">
        <div className="panel-body">
          <div className="row">
            <div className="col-xs-3 user-card-left">
              <div className="user-card-small-avatar">
                <span>
                  <Avatar size="50" size2x="80" />
                </span>
              </div>
            </div>
            <div className="col-xs-9 col-sm-12 user-card-body">
              <div className="user-card-avatar">
                <span>
                  <Avatar size="150" size2x="200" />
                </span>
              </div>

              <div className="user-card-username">
                <span
                  className="ui-preview-text"
                  style={{ width: random.int(60, 150) + "px" }}
                >
                  &nbsp;
                </span>
              </div>
              <div className="user-card-title">
                <span
                  className="ui-preview-text"
                  style={{ width: random.int(60, 150) + "px" }}
                >
                  &nbsp;
                </span>
              </div>

              <div className="user-card-stats">
                <ul className="list-unstyled">
                  <li>
                    <span
                      className="ui-preview-text"
                      style={{ width: random.int(30, 70) + "px" }}
                    >
                      &nbsp;
                    </span>
                  </li>
                  <li>
                    <span
                      className="ui-preview-text"
                      style={{ width: random.int(30, 70) + "px" }}
                    >
                      &nbsp;
                    </span>
                  </li>
                  <li className="user-stat-divider" />
                  <li>
                    <span
                      className="ui-preview-text"
                      style={{ width: random.int(30, 70) + "px" }}
                    >
                      &nbsp;
                    </span>
                  </li>
                  <li>
                    <span
                      className="ui-preview-text"
                      style={{ width: random.int(30, 70) + "px" }}
                    >
                      &nbsp;
                    </span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
