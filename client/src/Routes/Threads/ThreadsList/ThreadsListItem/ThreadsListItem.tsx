import React from "react"
import { Link } from "react-router-dom"
import * as urls from "../../../../urls"
import { IThread } from "../../Threads.types"
import ThreadsListItemLastActivity from "./ThreadsListItemLastActivity"
import ThreadsListItemLastPoster from "./ThreadsListItemLastPoster"
import ThreadsListItemSelect from "./ThreadsListItemSelect"
import ThreadsListItemStarter from "./ThreadsListItemStarter"
import ThreadsListItemTidbits from "./ThreadsListItemTidbits"

interface IThreadsListItemProps {
  selectable?: boolean
  selected?: boolean
  thread: IThread
  selectionChange: (id: string, selected: boolean) => void
}

const ThreadsListItem: React.FC<IThreadsListItemProps> = ({
  selectable,
  selected,
  selectionChange,
  thread,
}) => (
  <li className="list-group-item threads-list-item">
    <div className="row no-gutters">
      <ThreadsListItemStarter
        avatarSize={32}
        className="threads-list-starter-sm"
        thread={thread}
      />
      <ThreadsListItemStarter thread={thread} />
      <div className="col threads-list-thread">
        <Link className="threads-list-thread-title" to={urls.thread(thread)}>
          {thread.title}
        </Link>
        <ThreadsListItemTidbits thread={thread} />
      </div>
      <ThreadsListItemLastPoster thread={thread} />
      <ThreadsListItemLastActivity thread={thread} />
      {selectable && (
        <ThreadsListItemSelect
          selected={selected || false}
          onChange={(event) =>
            selectionChange(thread.id, event.target.checked)
          }
        />
      )}
    </div>
  </li>
)

export default React.memo(ThreadsListItem)
