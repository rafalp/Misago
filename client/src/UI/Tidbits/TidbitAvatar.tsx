import React from "react"
import { Link } from "react-router-dom"
import * as urls from "../../urls"
import { IAvatar } from "../../types"
import Avatar from "../Avatar"
import TidbitItem from "./TidbitItem"

interface TidbitAvatarProps {
  user?: {
    id: string
    slug: string
    name: string
    avatars: Array<IAvatar>
  } | null
  size?: number
}

const DEFAULT_SIZE = 24

const TidbitAvatar: React.FC<TidbitAvatarProps> = ({ user, size }) => (
  <TidbitItem className="tidbit-avatar">
    {user ? (
      <Link to={urls.user(user)}>
        <Avatar size={size || DEFAULT_SIZE} user={user} />
      </Link>
    ) : (
      <Avatar size={size || DEFAULT_SIZE} />
    )}
  </TidbitItem>
)

export default TidbitAvatar
