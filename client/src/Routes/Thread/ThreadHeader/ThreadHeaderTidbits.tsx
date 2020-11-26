import React from "react"
import {
  Tidbits,
  TidbitActivityLastReply,
  TidbitActivityStart,
  TidbitAvatar,
  TidbitCategory,
  TidbitClosed,
  TidbitReplies,
} from "../../../UI/Tidbits"
import * as urls from "../../../urls"
import { IThread } from "../Thread.types"

interface IThreadHeaderTidbitsProps {
  thread: IThread
}

const ThreadHeaderTidbits: React.FC<IThreadHeaderTidbitsProps> = ({
  thread,
}) => (
  <div className="row align-items-center justify-content-between">
    <div className="col-12 col-md-auto thread-header-tidbits-stats">
      <Tidbits>
        {thread.category.parent && (
          <TidbitCategory category={thread.category.parent} parent />
        )}
        <TidbitCategory category={thread.category} />
        <TidbitActivityStart
          date={new Date(thread.startedAt)}
          userName={thread.starterName}
          user={thread.starter}
          url={urls.thread(thread)}
        />
        {thread.replies > 0 && <TidbitReplies value={thread.replies} />}
        {thread.isClosed && <TidbitClosed />}
      </Tidbits>
    </div>
    <div className="col-12 col-md-auto thread-header-tidbit-last-activity">
      <Tidbits>
        <TidbitAvatar user={thread.lastPoster} />
        <TidbitActivityLastReply
          date={new Date(thread.lastPostedAt)}
          userName={thread.lastPosterName}
          user={thread.lastPoster}
          url={urls.threadLastPost(thread)}
        />
      </Tidbits>
    </div>
  </div>
)

export default React.memo(ThreadHeaderTidbits)
