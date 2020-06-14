import React from "react"
import { Link } from "react-router-dom"
import { Timestamp } from "../../../UI"
import * as urls from "../../../urls"
import { IPost } from "../Thread.types"

interface IThreadPostHeaderProps {
  post: IPost
}

const ThreadPostHeader: React.FC<IThreadPostHeaderProps> = ({ post }) => (
  <div className="card-header thread-post-header">
    {post.poster ? (
      <Link className="thread-post-poster" to={urls.user(post.poster)}>
        {post.poster.name}
      </Link>
    ) : (
      <span className="thread-post-poster">{post.posterName}</span>
    )}
    {" - "}
    <Timestamp date={new Date(post.postedAt)} />
  </div>
)

export default React.memo(ThreadPostHeader)
