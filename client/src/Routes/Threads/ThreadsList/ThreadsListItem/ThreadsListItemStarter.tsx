import classNames from "classnames"
import React from "react"
import { Link } from "react-router-dom"
import { Avatar } from "../../../../UI"
import * as urls from "../../../../urls"
import { IThread } from "../../Threads.types"

interface IThreadsListItemStarterProps {
  avatarSize?: number
  className?: string
  thread: IThread
}

const ThreadsListItemStarter: React.FC<IThreadsListItemStarterProps> = ({
  avatarSize,
  className,
  thread: { starter },
}) => (
  <div className={classNames("col-auto threads-list-starter", className)}>
    {starter ? (
      <Link to={urls.user(starter)}>
        <Avatar size={avatarSize || 40} user={starter} />
      </Link>
    ) : (
      <Avatar size={avatarSize || 40} />
    )}
  </div>
)

export default ThreadsListItemStarter
