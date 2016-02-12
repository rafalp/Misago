import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import * as random from 'misago/utils/random'; // jshint ignore:line

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="active-posters-list">
      <div className="container">
        <p className="lead ui-preview-paragraph">
          {random.range(3, 4).map((i) => {
            return <span key={i} className="ui-preview-text" style={{width: random.int(50, 120) + "px"}}>&nbsp;</span>
          })}
        </p>

        <div className="active-posters ui-preview">
          <ul className="list-group">
            {random.range(5, 10).map((i, counter) => {
              return <li key={i} className="list-group-item">
                <div className="rank-user-avatar">
                  <span>
                    <Avatar size="50" />
                  </span>
                </div>

                <div className="rank-user">
                  <div className="user-name">
                    <span className="item-title">
                      <span className="ui-preview-text" style={{width: random.int(30, 80) + "px"}}>&nbsp;</span>
                    </span>
                  </div>

                  <span className="user-status">
                    <span className="status-icon ui-preview">
                      &nbsp;
                    </span>
                    <span className="status-label ui-preview hidden-xs hidden-sm">
                      &nbsp;
                    </span>
                  </span>
                  <span className="rank-name">
                    <span className="ui-preview-text" style={{width: random.int(30, 50) + "px"}}>&nbsp;</span>
                  </span>
                  <span className="user-title hidden-xs hidden-sm">
                    <span className="ui-preview-text" style={{width: random.int(30, 50) + "px"}}>&nbsp;</span>
                  </span>
                </div>

                <div className="rank-position">
                  <strong>
                    <span className="ui-preview-text" style={{width: "30px"}}>&nbsp;</span>
                  </strong>
                  <small>{gettext("Rank")}</small>
                </div>

                <div className="rank-posts-counted">
                  <strong>
                    <span className="ui-preview-text" style={{width: "30px"}}>&nbsp;</span>
                  </strong>
                  <small>{gettext("Ranked posts")}</small>
                </div>

                <div className="rank-posts-total">
                  <strong>
                    <span className="ui-preview-text" style={{width: "30px"}}>&nbsp;</span>
                  </strong>
                  <small>{gettext("Total posts")}</small>
                </div>
              </li>;
            })}
          </ul>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}