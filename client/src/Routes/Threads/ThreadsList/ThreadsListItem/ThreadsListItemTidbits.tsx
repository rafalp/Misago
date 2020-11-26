import React from "react"
import {
  TidbitActivityLastReply,
  TidbitActivityStart,
  TidbitCategory,
  TidbitClosed,
  TidbitReplies,
  Tidbits,
} from "../../../../UI/Tidbits"
import * as urls from "../../../../urls"
import { IThread } from "../../Threads.types"

interface IThreadsListItemTidbitsProps {
  thread: IThread
}

const ThreadsListItemTidbits: React.FC<IThreadsListItemTidbitsProps> = ({
  thread,
}) => (
  <Tidbits>
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
      date={new Date(thread.lastPostedAt)}
      url={urls.threadLastPost(thread)}
      user={thread.lastPoster}
      userName={thread.lastPosterName}
    />
    <TidbitReplies value={thread.replies} />
    {thread.isClosed && <TidbitClosed />}
  </Tidbits>
)

export default ThreadsListItemTidbits
