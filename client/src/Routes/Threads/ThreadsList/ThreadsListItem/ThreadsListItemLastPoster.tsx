import classnames from "classnames"
import React from "react"
import { Link } from "react-router-dom"
import Avatar from "../../../../UI/Avatar"
import * as urls from "../../../../urls"
import { IThread } from "../../Threads.types"

interface IThreadsListItemLastPosterProps {
  avatarSize?: number
  className?: string
  thread: IThread
}

const ThreadsListItemLastPoster: React.FC<IThreadsListItemLastPosterProps> = ({
  avatarSize,
  className,
  thread: { lastPoster },
}) => (
  <div
    className={classnames("col-auto", className || "threads-list-last-poster")}
  >
    {lastPoster ? (
      <Link to={urls.user(lastPoster)}>
        <Avatar size={avatarSize || 40} user={lastPoster} />
      </Link>
    ) : (
      <Avatar size={avatarSize || 40} />
    )}
  </div>
)

export default ThreadsListItemLastPoster
