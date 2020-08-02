import React from "react"
import { ModalAlert, ModalErrorBody } from "../../../../UI"
import { IMutationError } from "../../../../types"
import ThreadRootError from "../../ThreadRootError"
import { IPost } from "../../Thread.types"
import ThreadPostsModerationErrorHeader from "./ThreadPostsModerationErrorHeader"
import ThreadPostsModerationErrorPosts from "./ThreadPostsModerationErrorPosts"

interface IThreadPostsModerationErrorProps {
  forDelete?: boolean
  posts: Array<IPost>
  errors: Array<IMutationError>
  selectionErrors: Record<string, IMutationError>
}

const ThreadPostsModerationError: React.FC<IThreadPostsModerationErrorProps> = ({
  forDelete,
  posts,
  errors,
  selectionErrors,
}) => {
  if (selectionErrors) {
    return (
      <>
        <ModalAlert>
          <ThreadPostsModerationErrorHeader
            forDelete={forDelete}
            posts={posts}
            postsErrors={selectionErrors}
          />
        </ModalAlert>
        <ThreadPostsModerationErrorPosts
          posts={posts}
          errors={selectionErrors}
        />
      </>
    )
  }

  return (
    <ThreadRootError dataErrors={errors}>
      {({ message }) => (
        <ModalErrorBody
          header={
            <ThreadPostsModerationErrorHeader
              forDelete={forDelete}
              posts={posts}
              postsErrors={selectionErrors}
            />
          }
          message={message}
        />
      )}
    </ThreadRootError>
  )
}

export default ThreadPostsModerationError
