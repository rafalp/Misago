import classNames from "classnames"
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
  changeSelection: (id: string, selected: boolean) => void
  selectable?: boolean
  selected?: boolean
  thread: IThread
}

const ThreadsListItem: React.FC<IThreadsListItemProps> = ({
  changeSelection,
  selectable,
  selected,
  thread,
}) => (
  <li
    className={classNames("list-group-item threads-list-item", {
      "threads-list-item-with-replies": thread.replies > 0,
      "threads-list-item-without-replies": thread.replies === 0,
    })}
  >
    <div className="row no-gutters">
      <ThreadsListItemStarter thread={thread} />
      <ThreadsListItemLastPoster
        avatarSize={32}
        className="threads-list-last-poster-sm"
        thread={thread}
      />
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
            changeSelection(thread.id, event.target.checked)
          }
        />
      )}
    </div>
  </li>
)

export default React.memo(ThreadsListItem)
