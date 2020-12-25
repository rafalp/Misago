import { ApolloError } from "apollo-client"
import React from "react"
import RootError from "../../../UI/RootError"
import {
  PostValidationError,
  ThreadValidationError,
} from "../../../UI/ValidationError"
import useLocationError from "../../../UI/useLocationError"
import useRootError from "../../../UI/useRootError"
import { MutationError } from "../../../types"

interface Error {
  message: React.ReactNode
  type: string
}

interface ThreadPostRootErrorProps {
  children: (error: Error) => React.ReactElement
  dataErrors?: Array<MutationError> | null
  graphqlError?: ApolloError | null
}

const ThreadPostRootError: React.FC<ThreadPostRootErrorProps> = ({
  children,
  dataErrors,
  graphqlError,
}) => {
  const rootError = useRootError(dataErrors)
  const threadError = useLocationError("thread", dataErrors)
  const postError = useLocationError("post", dataErrors)

  if (graphqlError) {
    return <RootError graphqlError={graphqlError}>{children}</RootError>
  }

  if (rootError) {
    return <RootError dataErrors={[rootError]}>{children}</RootError>
  }

  if (threadError) {
    return (
      <ThreadValidationError error={threadError}>
        {children}
      </ThreadValidationError>
    )
  }

  if (postError) {
    return (
      <PostValidationError error={postError}>{children}</PostValidationError>
    )
  }

  return null
}

export default ThreadPostRootError
