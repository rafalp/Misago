import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import * as random from 'misago/utils/random'; // jshint ignore:line

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div>
      <div className="users-cards-list">
        <div className="row">
          {[0, 1, 2, 3].map((i) => {
            return <div className="col-md-3" key={i}>
              <div className='user-card ui-preview'>
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

                        <span className="user-status">
                          <span className="status-icon ui-preview">
                            &nbsp;
                          </span>
                          <span className="status-label ui-preview">
                            &nbsp;
                          </span>
                        </span>
                        <span className="user-joined-on">
                          <span className="ui-preview-text" style={{width: random.int(30, 50) + "px"}}>&nbsp;</span>
                        </span>

                      </p>

                    </div>
                  </div>
                </div>
              </div>
            </div>;
          })}
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}
