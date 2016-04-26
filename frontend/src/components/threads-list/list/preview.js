import React from 'react';
import ThreadPreview from 'misago/components/threads-list/thread/preview'; // jshint ignore:line

export default class extends React.Component {
  shouldComponentUpdate() {
    return false;
  }

  render () {
    /* jshint ignore:start */
    return <div className="threads-list ui-preview">
      <ul className="list-group">
        {[0, 1, 2].map((i) => {
          return <ThreadPreview hiddenOnMobile={i > 0} key={i} />
        })}
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}