import React from "react"
import ThreadsListItem from "./ThreadsListItem";
import ThreadsListLoader from "./ThreadsListLoader";

const ThreadsList = ({
  category,
  categories,
  threads,
  busyThreads,
  isLoaded,
  showOptions,
  selection,
}) => {
  if (!isLoaded) {
    return <ThreadsListLoader showOptions={showOptions} />
  }

  return (
    <div className="threads-list">
      <ul className="list-group">
        {threads.map(
          thread => (
            <ThreadsListItem
              key={thread.id}
              activeCategory={category}
              categories={categories}
              thread={thread}
              showOptions={showOptions}
              isBusy={busyThreads.indexOf(thread.id) >= 0}
              isSelected={selection.indexOf(thread.id) >= 0}
            />
          )
        )}
      </ul>
    </div>
  )
}

export default ThreadsList