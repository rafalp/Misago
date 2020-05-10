import React from "react"
import { Link } from "react-router-dom"
import { Avatar } from "../../../../UI"
import * as urls from "../../../../urls"
import { IThread } from "../../Threads.types"

interface IThreadsListItemStarterProps {
  thread: IThread
}

const ThreadsListItemStarter: React.FC<IThreadsListItemStarterProps> = ({
  thread: { starter },
}) => (
  <div className="col-auto threads-list-starter">
    {starter ? (
      <Link to={urls.user(starter)}>
        <Avatar size={40} user={starter} />
      </Link>
    ) : (
      <Avatar size={40} />
    )}
  </div>
)

export default ThreadsListItemStarter
