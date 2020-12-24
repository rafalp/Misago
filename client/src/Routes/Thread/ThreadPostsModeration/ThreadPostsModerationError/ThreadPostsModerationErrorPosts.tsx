import React from "react"
import { ModalBody } from "../../../../UI/Modal"
import Timestamp from "../../../../UI/Timestamp"
import { PostValidationError } from "../../../../UI/ValidationError"
import RichText from "../../../../UI/RichText"
import { MutationError } from "../../../../types"
import { IPost } from "../../Thread.types"

interface IThreadPostsModerationErrorPostsProps {
  errors: Record<string, MutationError>
  posts: Array<IPost>
}

const ThreadPostsModerationErrorPosts: React.FC<IThreadPostsModerationErrorPostsProps> = ({
  posts,
  errors,
}) => (
  <ModalBody className="modal-posts-errors">
    <ul className="posts-errors">
      {posts.map((post) => {
        if (!errors[post.id]) return null

        return (
          <li key={post.id} className="post-errors-post">
            <PostValidationError error={errors[post.id]}>
              {({ message }) => (
                <div className="posts-errors-post-error">{message}</div>
              )}
            </PostValidationError>
            <div className="selected-post-header">
              <span className="posts-errors-post-poster">
                {post.poster ? post.poster.name : post.posterName}
              </span>
              <span className="posts-errors-post-timestamp">
                <Timestamp date={new Date(post.postedAt)} />
              </span>
            </div>
            <div className="posts-errors-post-body">
              <RichText richText={post.richText} />
            </div>
          </li>
        )
      })}
    </ul>
  </ModalBody>
)

export default ThreadPostsModerationErrorPosts
