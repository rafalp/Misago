import React from 'react';
import ChangePreview from 'misago/components/username-history/change-preview'; // jshint ignore:line

export default class extends React.Component {
  shouldComponentUpdate() {
    return false;
  }

  render () {
    /* jshint ignore:start */
    return <div className="username-history ui-preview">
      <ul className="list-group">
        {[0, 1, 2].map((i) => {
          return <ChangePreview hiddenOnMobile={i > 0} key={i} />
        })}
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}