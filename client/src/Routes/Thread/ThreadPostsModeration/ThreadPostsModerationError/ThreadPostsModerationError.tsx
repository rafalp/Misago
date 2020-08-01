import React from "react"
import {
  ModalAlert,
  ModalErrorBody,
  RootError,
  ThreadValidationError,
  useLocationError,
  useRootError,
} from "../../../../UI"
import { IMutationError } from "../../../../types"
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
  const threadError = useLocationError("thread", errors)
  const rootError = useRootError(errors)

  if (rootError) {
    return (
      <RootError dataErrors={[rootError]}>
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
      </RootError>
    )
  }

  if (threadError) {
    return (
      <ThreadValidationError error={threadError}>
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
      </ThreadValidationError>
    )
  }

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

  return null
}

export default ThreadPostsModerationError
