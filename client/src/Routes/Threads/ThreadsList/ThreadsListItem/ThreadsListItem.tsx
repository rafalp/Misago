import React from "react"
import { Link } from "react-router-dom"
import {
  Avatar,
  TidbitActivityLastReply,
  TidbitActivityStart,
  TidbitCategory,
  TidbitClosed,
  TidbitReplies,
  Tidbits,
} from "../../../../UI"
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
          <TidbitActivityStart
            date={new Date(thread.startedAt)}
            url={urls.thread(thread)}
            user={thread.starter}
            userName={thread.starterName}
          />
          <TidbitActivityLastReply
            date={new Date(thread.startedAt)}
            url={urls.threadLastReply(thread)}
            user={thread.starter}
            userName={thread.starterName}
          />
          <TidbitReplies value={thread.replies} />
          {thread.isClosed && <TidbitClosed />}
        </Tidbits>
      </div>
      <ThreadsListItemLastPoster thread={thread} />
      <ThreadsListItemLastActivity thread={thread} />
    </div>
  </li>
)

export default ThreadsListItem
