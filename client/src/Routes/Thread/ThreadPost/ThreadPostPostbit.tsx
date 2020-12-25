import React from "react"
import { Link } from "react-router-dom"
import Avatar from "../../../UI/Avatar"
import * as urls from "../../../urls"
import { Post } from "../Thread.types"

interface ThreadPostPostbitProps {
  post: Post
}

const AVATAR_SIZE = 100

const ThreadPostPostbit: React.FC<ThreadPostPostbitProps> = ({ post }) => (
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
