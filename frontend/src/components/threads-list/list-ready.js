import React from 'react';
import Thread from 'misago/components/threads-list/thread'; // jshint ignore:line

export default class extends React.Component {
  render () {
    /* jshint ignore:start */
    return <div className="threads-list ui-ready">
      <ul className="list-group">
        {this.props.threads.map((thread) => {
          return <Thread categories={this.props.categories}
                         thread={thread}
                         list={this.props.list}
                         key={thread.id} />
        })}
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}