import React from "react"
import ThreadsListEmpty from "./ThreadsListEmpty"
import ThreadsListItem from "./ThreadsListItem"
import ThreadsListLoader from "./ThreadsListLoader"
import ThreadsListUpdatePrompt from "./ThreadsListUpdatePrompt"

const ThreadsList = ({
  list,
  categories,
  category,
  threads,
  busyThreads,
  selection,
  isLoaded,
  showOptions,
  updatedThreads,
  applyUpdate,
  emptyMessage,
}) => {
  if (!isLoaded) {
    return <ThreadsListLoader showOptions={showOptions} />
  }

  return (
    <div className="threads-list">
      {threads.length > 0 ? (
        <ul className="list-group">
          {updatedThreads > 0 && (
            <ThreadsListUpdatePrompt
              threads={updatedThreads}
              onClick={applyUpdate}
            />
          )}
          {threads.map((thread) => (
            <ThreadsListItem
              key={thread.id}
              activeCategory={category}
              categories={categories}
              thread={thread}
              showOptions={showOptions}
              showNotifications={showOptions && list.type === "watched"}
              isBusy={busyThreads.indexOf(thread.id) >= 0}
              isSelected={selection.indexOf(thread.id) >= 0}
            />
          ))}
        </ul>
      ) : (
        <ul className="list-group">
          {updatedThreads > 0 && (
            <ThreadsListUpdatePrompt
              threads={updatedThreads}
              onClick={applyUpdate}
            />
          )}
          <ThreadsListEmpty
            category={category}
            list={list}
            message={emptyMessage}
          />
        </ul>
      )}
    </div>
  )
}

export default ThreadsList
