import React from "react"
import ThreadsListItem from "./ThreadsListItem";

const ThreadsList = ({ threads, isLoaded }) => {
  if (!isLoaded) {
    return <div>LOADING THREADS</div>
  }

  return (
    <div className="threads-list">
      <ul className="list-group">
        {threads.map(
          thread => <ThreadsListItem key={thread.id} thread={thread} />
        )}
      </ul>
    </div>
  )
}

export default ThreadsList