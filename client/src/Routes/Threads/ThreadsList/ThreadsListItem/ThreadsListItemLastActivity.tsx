import React from "react"
import { TidbitTimestamp, TidbitUser, Tidbits } from "../../../../UI/Tidbits"
import * as urls from "../../../../urls"
import { Thread } from "../../Threads.types"

interface ThreadsListItemLastActivityProps {
  thread: Thread
}

const ThreadsListItemLastActivity: React.FC<ThreadsListItemLastActivityProps> = ({
  thread,
}) => (
  <div className="col-auto threads-list-activity">
    <Tidbits vertical>
      <TidbitUser name={thread.lastPosterName} user={thread.lastPoster} />
      <TidbitTimestamp
        date={new Date(thread.lastPostedAt)}
        url={urls.threadLastPost(thread)}
      />
    </Tidbits>
  </div>
)

export default ThreadsListItemLastActivity
