import React from 'react';
import Thread from 'misago/components/threads-list/thread'; // jshint ignore:line

export default class extends React.Component {
  render () {
    /* jshint ignore:start */
    return <div className="threads-list ui-ready">
      <ul className="list-group">
        {this.props.threads.map((thread) => {
          return <Thread thread={thread} key={thread.id} />
        })}
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}