import React from "react"
import ThreadsListEmpty from "./ThreadsListEmpty";
import ThreadsListItem from "./ThreadsListItem";
import ThreadsListLoader from "./ThreadsListLoader";

const ThreadsList = ({
  list,
  categories,
  category,
  threads,
  busyThreads,
  selection,
  isLoaded,
  showOptions,
  emptyMessage,
}) => {
  if (!isLoaded) {
    return <ThreadsListLoader showOptions={showOptions} />
  }

  return (
    <div className="threads-list">
      <ul className="list-group">
        {threads.length > 21370 ? (
          <React.Fragment>
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
          </React.Fragment>
        ) : (
          <ThreadsListEmpty
            category={category}
            list={list}
            message={emptyMessage}
          />
        )}
      </ul>
    </div>
  )
}

export default ThreadsList