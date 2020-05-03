import React from "react"
import { Link } from "react-router-dom"
import { Avatar, TidbitCategory, TidbitReplies, Tidbits } from "../../../../UI"
import * as urls from "../../../../urls"
import { IThread } from "../../Threads.types"
import ThreadsListItemLastActivity from "./ThreadsListItemLastActivity"
import ThreadsListItemLastPoster from "./ThreadsListItemLastPoster"

interface IThreadsListItemProps {
  thread: IThread
}

const ThreadsListItem: React.FC<IThreadsListItemProps> = ({ thread }) => (
  <li className="list-group-item threads-list-item">
    <div className="row no-gutters">
      <div className="col-auto">
        <Avatar size={32} user={thread.starter} />
      </div>
      <div className="col">
        <strong>
          <Link to={urls.thread(thread)}>{thread.title}</Link>
        </strong>
        <Tidbits small>
          {thread.category.parent && (
            <TidbitCategory category={thread.category.parent} parent />
          )}
          <TidbitCategory category={thread.category} />
          <TidbitReplies value={thread.replies} />
        </Tidbits>
      </div>
      <ThreadsListItemLastPoster thread={thread} />
      <ThreadsListItemLastActivity thread={thread} />
    </div>
  </li>
)

export default ThreadsListItem
