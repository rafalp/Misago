import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import * as random from 'misago/utils/random'; // jshint ignore:line

export default class extends React.Component {
  shouldComponentUpdate() {
    return false;
  }

  getUserStatus() {
    if (this.props.showStatus) {
      /* jshint ignore:start */
      return <span className="user-status">
        <span className="status-icon ui-preview-text">
          &nbsp;
        </span>
        <span className="status-label ui-preview-text"
              style={{width: random.int(30, 50) + "px"}}>
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
                <span className="ui-preview-text"
                      style={{width: random.int(60, 150) + "px"}}>
                  &nbsp;
                </span>
              </span>
            </h4>

            <p className="user-subscript">

              {this.getUserStatus()}
              <span className="user-joined-on">
                <span className="ui-preview-text"
                      style={{width: random.int(30, 50) + "px"}}>
                  &nbsp;
                </span>
              </span>

            </p>

          </div>
          <div className="user-card-stats">

            <ul className="list-unstyled">
              <li className="user-posts-count">
                <span className="ui-preview-text"
                      style={{width: random.int(40, 70) + "px"}}>
                  &nbsp;
                </span>
              </li>
              <li className="user-threads-count">
                <span className="ui-preview-text"
                      style={{width: random.int(40, 70) + "px"}}>
                  &nbsp;
                </span>
              </li>
              <li className="user-followers-count">
                <span className="ui-preview-text"
                      style={{width: random.int(40, 70) + "px"}}>
                  &nbsp;
                </span>
              </li>
            </ul>

          </div>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}