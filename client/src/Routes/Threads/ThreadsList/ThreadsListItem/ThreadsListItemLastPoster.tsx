import React from "react"
import { Link } from "react-router-dom"
import { Avatar } from "../../../../UI"
import * as urls from "../../../../urls"
import { IThread } from "../../Threads.types"

interface IThreadsListItemLastPosterProps {
  thread: IThread
}

const ThreadsListItemLastPoster: React.FC<IThreadsListItemLastPosterProps> = ({
  thread: { lastPoster },
}) => (
  <div className="col-auto threads-list-last-poster">
    {lastPoster ? (
      <Link to={urls.user(lastPoster)}>
        <Avatar size={32} user={lastPoster} />
      </Link>
    ) : (
      <Avatar size={32} />
    )}
  </div>
)

export default ThreadsListItemLastPoster
