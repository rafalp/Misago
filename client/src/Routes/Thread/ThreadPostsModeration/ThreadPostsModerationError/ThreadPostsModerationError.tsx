import React from "react"
import {
  ModalAlert,
  ModalCloseFooter,
  ModalErrorBody,
} from "../../../../UI/Modal"
import RootError from "../../../../UI/RootError"
import { ThreadValidationError } from "../../../../UI/ValidationError"
import useLocationError from "../../../../UI/useLocationError"
import useRootError from "../../../../UI/useRootError"
import { MutationError } from "../../../../types"
import { Post } from "../../Thread.types"
import ThreadPostsModerationErrorHeader from "./ThreadPostsModerationErrorHeader"
import ThreadPostsModerationErrorPosts from "./ThreadPostsModerationErrorPosts"

interface ThreadPostsModerationErrorProps {
  forDelete?: boolean
  posts: Array<Post>
  errors: Array<MutationError>
  selectionErrors: Record<string, MutationError>
  close: () => void
}

const ThreadPostsModerationError: React.FC<ThreadPostsModerationErrorProps> = ({
  forDelete,
  posts,
  errors,
  selectionErrors,
  close,
}) => {
  const rootError = useRootError(errors)
  const threadError = useLocationError("thread", errors)

  if (rootError) {
    return (
      <>
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
        <ModalCloseFooter close={close} />
      </>
    )
  }

  if (threadError) {
    return (
      <>
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
        <ModalCloseFooter close={close} />
      </>
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
        <ModalCloseFooter close={close} />
      </>
    )
  }

  return null
}

export default ThreadPostsModerationError
