import React from "react"
import { Link } from "react-router-dom"
import Avatar from "../../../UI/Avatar"
import * as urls from "../../../urls"
import { IPost } from "../Thread.types"

interface IThreadPostPostbitProps {
  post: IPost
}

const AVATAR_SIZE = 100

const ThreadPostPostbit: React.FC<IThreadPostPostbitProps> = ({ post }) => (
  <div className="thread-post-postbit">
    {post.poster ? (
      <Link to={urls.user(post.poster)}>
        <Avatar size={AVATAR_SIZE} user={post.poster} />
      </Link>
    ) : (
      <Avatar size={AVATAR_SIZE} />
    )}
  </div>
)

export default React.memo(ThreadPostPostbit)
