/* jshint ignore:start */
import React from 'react';
import * as random from 'misago/utils/random';

export default function(props) {
  return (
    <li className="post post-infeed">
      <div className="post-border">
        <div className="post-body">
          <div className="panel panel-default panel-post">
            <div className="panel-heading post-heading">
              <span className="ui-preview-text" style={{width: random.int(20, 50) + "%"}}>&nbsp;</span>
              <span className="ui-preview-text" style={{width: random.int(30, 100) + "px"}}>&nbsp;</span>
            </div>
            <div className="panel-body">
              <article className="misago-markup">
                <p className="ui-preview-text" style={{width: random.int(30, 100) + "%"}}>&nbsp;</p>
                <p className="ui-preview-text" style={{width: random.int(30, 100) + "%"}}>&nbsp;</p>
                <p className="ui-preview-text" style={{width: random.int(30, 100) + "%"}}>&nbsp;</p>
              </article>
            </div>
          </div>
        </div>
      </div>
    </li>
  );
}
