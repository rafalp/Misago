import { Trans } from "@lingui/macro"
import React from "react"
import { MutationError } from "../../../../types"
import { IPost } from "../../Thread.types"

interface IThreadPostsModerationErrorHeaderProps {
  forDelete?: boolean
  posts?: Array<IPost>
  postsErrors?: Record<string, MutationError>
}

const ThreadPostsModerationErrorHeader: React.FC<IThreadPostsModerationErrorHeaderProps> = ({
  forDelete,
  posts,
  postsErrors,
}) => {
  if (forDelete) {
    return (
      <ThreadPostsModerationErrorHeaderForDelete
        posts={posts}
        postsErrors={postsErrors}
      />
    )
  }

  return (
    <ThreadPostsModerationErrorHeaderForUpdate
      posts={posts}
      postsErrors={postsErrors}
    />
  )
}

const ThreadPostsModerationErrorHeaderForDelete: React.FC<IThreadPostsModerationErrorHeaderProps> = ({
  posts,
  postsErrors,
}) => {
  const errorsCount = postsErrors ? Object.keys(postsErrors).length : 0

  if (posts) {
    if (posts.length === 1) {
      return (
        <Trans id="moderation.selected_post_delete_error">
          Selected post could not be deleted.
        </Trans>
      )
    } else if (errorsCount > 0 && errorsCount < posts.length) {
      return (
        <Trans id="moderation.selected_posts_delete_error_some">
          Some of the selected posts could not be deleted.
        </Trans>
      )
    }
  }

  return (
    <Trans id="moderation.selected_posts_delete_error">
      Selected posts could not be deleted.
    </Trans>
  )
}

const ThreadPostsModerationErrorHeaderForUpdate: React.FC<IThreadPostsModerationErrorHeaderProps> = ({
  posts,
  postsErrors,
}) => {
  const errorsCount = postsErrors ? Object.keys(postsErrors).length : 0

  if (posts) {
    if (posts.length === 1) {
      return (
        <Trans id="moderation.selected_post_delete">
          Selected post could not be updated.
        </Trans>
      )
    } else if (errorsCount > 0 && errorsCount < posts.length) {
      return (
        <Trans id="moderation.selected_posts_error_some">
          Some of the selected posts could not be updated.
        </Trans>
      )
    }
  }

  return (
    <Trans id="moderation.selected_posts_error">
      Selected posts could not be updated.
    </Trans>
  )
}

export default ThreadPostsModerationErrorHeader
