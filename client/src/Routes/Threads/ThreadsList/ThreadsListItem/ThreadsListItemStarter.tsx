import React from "react"
import { Link } from "react-router-dom"
import Avatar from "../../../../UI/Avatar"
import * as urls from "../../../../urls"
import { Thread } from "../../Threads.types"

interface ThreadsListItemStarterProps {
  thread: Thread
}

const ThreadsListItemStarter: React.FC<ThreadsListItemStarterProps> = ({
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
