import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import * as random from 'misago/utils/random'; // jshint ignore:line

export default class extends React.Component {
  getUserStatus() {
    if (this.props.showStatus) {
      /* jshint ignore:start */
      return <span className="user-status">
        <span className="status-icon ui-preview">
          &nbsp;
        </span>
        <span className="status-label ui-preview">
          &nbsp;
        </span>
      </span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className='user-card ui-preview'>
      <div className="user-card-bg-image">
        <Avatar size="400" className="bg-image" />

        <div className="user-card-bg">
          <div className="user-details">

            <div className="user-avatar">
              <Avatar size="400" />
            </div>

            <h4 className="user-name">
              <span className="item-title">
                <span className="ui-preview-text" style={{width: random.int(60, 150) + "px"}}>&nbsp;</span>
              </span>
            </h4>

            <p className="user-subscript">

              {this.getUserStatus()}
              <span className="user-joined-on">
                <span className="ui-preview-text" style={{width: random.int(30, 50) + "px"}}>&nbsp;</span>
              </span>

            </p>

          </div>
          <div className="user-card-stats">

            <ul className="list-unstyled">
              <li className="user-posts-count">
                <strong>
                  <span className="ui-preview-text">&nbsp;</span>
                </strong>
                <small>{gettext("posts")}</small>
              </li>
              <li className="user-threads-count">
                <strong>
                  <span className="ui-preview-text">&nbsp;</span>
                </strong>
                <small>{gettext("threads")}</small>
              </li>
              <li className="user-followers-count">
                <strong>
                  <span className="ui-preview-text">&nbsp;</span>
                </strong>
                <small>{gettext("followers")}</small>
              </li>
            </ul>

          </div>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}