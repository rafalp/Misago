import React from "react"
import ThreadsListItem from "./ThreadsListItem";

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
    return <div>LOADING THREADS</div>
  }

  console.log(selection)

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
            />
          )
        )}
      </ul>
    </div>
  )
}

export default ThreadsList