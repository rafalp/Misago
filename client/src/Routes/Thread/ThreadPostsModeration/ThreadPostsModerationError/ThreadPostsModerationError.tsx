import React from "react"
import {
  ModalAlert,
  ModalCloseFooter,
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
  close: () => void
}

const ThreadPostsModerationError: React.FC<IThreadPostsModerationErrorProps> = ({
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
