/* jshint ignore:start */
import React from 'react';
import DiffMessage from 'misago/components/threads-list/list/diff-message'; // jshint ignore:line
import Thread from 'misago/components/threads-list/thread/ready'; // jshint ignore:line

export default function(props) {
  return (
    <div className="threads-list ui-ready">
      <ul className="list-group">
        <DiffMessage
          diffSize={props.diffSize}
          applyDiff={props.applyDiff}
        />
        {props.threads.map((thread) => {
          return (
            <Thread
              categories={props.categories}
              thread={thread}
              list={props.list}

              showOptions={props.showOptions}
              isSelected={props.selection.indexOf(thread.id) >= 0}

              isBusy={props.busyThreads.indexOf(thread.id) >= 0}
              key={thread.id}
            />
          );
        })}
      </ul>
    </div>
  );
}