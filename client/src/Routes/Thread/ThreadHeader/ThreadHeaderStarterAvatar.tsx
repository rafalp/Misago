import React from "react"
import { Link } from "react-router-dom"
import Avatar from "../../../UI/Avatar"
import * as urls from "../../../urls"
import { IThreadPoster } from "../Thread.types"

interface IThreadHeaderStarterAvatarProps {
  starter: IThreadPoster | null
}

const AVATAR_SIZE = 64

const ThreadHeaderStarterAvatar: React.FC<IThreadHeaderStarterAvatarProps> = ({
  starter,
}) => (
  <div className="thread-header-starter-avatar">
    {starter ? (
      <Link to={urls.user(starter)}>
        <Avatar size={AVATAR_SIZE} user={starter} />
      </Link>
    ) : (
      <Avatar size={AVATAR_SIZE} />
    )}
  </div>
)

export default ThreadHeaderStarterAvatar
