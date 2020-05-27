import React from "react"
import { TidbitCategory, TidbitReplies, Tidbits } from "../../../../UI"
import { ISelectedThread } from "./ThreadsModerationSelectedThreads.types"

interface IThreadsModerationSelectedThreadsListProps {
  threads: Array<ISelectedThread>
}

const ThreadsModerationSelectedThreadsList: React.FC<IThreadsModerationSelectedThreadsListProps> = ({
  threads,
}) => (
  <ul className="list-unstyled selected-threads-list">
    {threads.map((thread) => (
      <li
        className="list-group-item selected-threads-list-item"
        key={thread.id}
      >
        <div className="selected-thread-title">{thread.title}</div>
        <Tidbits small>
          {thread.category.parent && (
            <TidbitCategory
              category={thread.category.parent}
              disabled
              parent
            />
          )}
          <TidbitCategory category={thread.category} disabled />
          {thread.replies > 0 && <TidbitReplies value={thread.replies} />}
        </Tidbits>
      </li>
    ))}
  </ul>
)

export default ThreadsModerationSelectedThreadsList
