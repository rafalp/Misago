import React from "react"
import DiffMessage from "misago/components/threads-list/list/diff-message"
import Thread from "misago/components/threads-list/thread/ready"

export default function(props) {
  return (
    <div className="threads-list ui-ready">
      <ul className="list-group">
        <DiffMessage diffSize={props.diffSize} applyDiff={props.applyDiff} />
        {props.threads.map(thread => (
          <Thread
            activeCategory={props.activeCategory}
            categories={props.categories}
            list={props.list}
            thread={thread}
            showOptions={props.showOptions}
            isSelected={props.selection.indexOf(thread.id) >= 0}
            isBusy={props.busyThreads.indexOf(thread.id) >= 0}
            key={thread.id}
          />
        ))}
      </ul>
    </div>
  )
}
