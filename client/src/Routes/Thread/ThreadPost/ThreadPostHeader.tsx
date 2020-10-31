import { Plural } from "@lingui/macro"
import React from "react"
import { Link } from "react-router-dom"
import Avatar from "../../../UI/Avatar"
import { Checkbox } from "../../../UI/Checkbox"
import Timestamp from "../../../UI/Timestamp"
import * as urls from "../../../urls"
import { IPost } from "../Thread.types"
import ThreadPostOptions from "./ThreadPostOptions"
import { useThreadPostModeration } from "./ThreadPostModeration"

interface IThreadPostHeaderProps {
  acl: { edit: boolean }
  post: IPost
  threadId: string
  threadSlug: string
  page?: number
  isSelected?: boolean
  editPost: () => void
  toggleSelection?: ((id: string) => void) | null
}

const ThreadPostHeader: React.FC<IThreadPostHeaderProps> = ({
  acl,
  post,
  threadId,
  threadSlug,
  page,
  isSelected,
  editPost,
  toggleSelection,
}) => {
  const moderation = useThreadPostModeration(threadId, post, page)

  return (
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
            <Link
              className="post-timestamp"
              to={urls.threadPost({ id: threadId, slug: threadSlug }, post)}
            >
              <Timestamp date={new Date(post.postedAt)} />
            </Link>
            {post.edits > 0 && (
              <>
                <span className="post-header-dash">&ndash;</span>
                <span className="post-header-edits">
                  <Plural
                    id="edits"
                    value={post.edits}
                    one="# edit"
                    other="# edits"
                  />
                </span>
              </>
            )}
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
          <ThreadPostOptions
            acl={acl}
            post={post}
            threadId={threadId}
            threadSlug={threadSlug}
            moderation={moderation}
            editPost={editPost}
          />
        </div>
        {toggleSelection && (
          <div className="col-auto post-header-select">
            <Checkbox
              checked={isSelected}
              onChange={() => toggleSelection(post.id)}
            />
          </div>
        )}
      </div>
    </div>
  )
}

export default React.memo(ThreadPostHeader)
