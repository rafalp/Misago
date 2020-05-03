import React from "react"
import { TidbitTimestamp, TidbitUser, Tidbits } from "../../../../UI"
import * as urls from "../../../../urls"
import { IThread } from "../../Threads.types"

interface IThreadsListItemLastActivityProps {
  thread: IThread
}

const ThreadsListItemLastActivity: React.FC<IThreadsListItemLastActivityProps> = ({
  thread,
}) => (
  <div className="col-auto threads-list-activity">
    <Tidbits small vertical>
      <TidbitUser name={thread.lastPosterName} user={thread.lastPoster} />
      <TidbitTimestamp
        date={new Date(thread.lastPostedAt)}
        url={urls.threadLastReply(thread)}
      />
    </Tidbits>
  </div>
)

export default ThreadsListItemLastActivity
