import React from "react"
import { Link } from "react-router-dom"
import { Avatar, ButtonSecondary, Timestamp } from "../../../UI"
import * as urls from "../../../urls"
import { IPost } from "../Thread.types"

interface IThreadPostHeaderProps {
  post: IPost
}

const ThreadPostHeader: React.FC<IThreadPostHeaderProps> = ({ post }) => (
  <div className="card-header post-header">
    <div className="row align-items-center no-gutters">
      <div className="col-auto post-avatar-sm">
        {post.poster ? (
          <Link className="post-poster-avatar" to={urls.user(post.poster)}>
            <Avatar size={32} user={post.poster} />
          </Link>
        ) : (
          <span className="post-poster-avatar">
            <Avatar size={32} />
          </span>
        )}
      </div>
      <div className="col">
        <div className="post-header-full">
          {post.poster ? (
            <Link className="post-poster" to={urls.user(post.poster)}>
              {post.poster.name}
            </Link>
          ) : (
            <span className="post-poster">{post.posterName}</span>
          )}
          <span className="post-header-dash">&ndash;</span>
          <Link className="post-timestamp" to={"/"}>
            <Timestamp date={new Date(post.postedAt)} />
          </Link>
        </div>
        <div className="post-header-compact">
          <div className="post-header-first-row">
            {post.poster ? (
              <Link className="post-poster" to={urls.user(post.poster)}>
                {post.poster.name}
              </Link>
            ) : (
              <span className="post-poster">{post.posterName}</span>
            )}
          </div>
          <div className="post-header-second-row">
            <Link className="post-timestamp" to={"/"}>
              <Timestamp date={new Date(post.postedAt)} />
            </Link>
          </div>
        </div>
      </div>
      <div className="col-auto">
        <ButtonSecondary
          icon="ellipsis-h"
          iconSolid
          small
          onClick={() => {}}
        />
      </div>
    </div>
  </div>
)

export default React.memo(ThreadPostHeader)
