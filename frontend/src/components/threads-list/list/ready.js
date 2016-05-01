import React from 'react';
import DiffMessage from 'misago/components/threads-list/list/diff-message'; // jshint ignore:line
import Thread from 'misago/components/threads-list/thread/ready'; // jshint ignore:line

export default class extends React.Component {
  getDiffMessage() {
    if (this.props.diffSize > 0) {
      /* jshint ignore:start */
      return <DiffMessage diffSize={this.props.diffSize}
                          applyDiff={this.props.applyDiff} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render () {
    /* jshint ignore:start */
    return <div className="threads-list ui-ready">
      <ul className="list-group">
        {this.getDiffMessage()}
        {this.props.threads.map((thread) => {
          return <Thread categories={this.props.categories}
                         thread={thread}
                         list={this.props.list}

                         showOptions={this.props.showOptions}
                         isSelected={this.props.selection.indexOf(thread.id) >= 0}

                         isBusy={this.props.busyThreads.indexOf(thread.id) >= 0}
                         key={thread.id} />
        })}
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}