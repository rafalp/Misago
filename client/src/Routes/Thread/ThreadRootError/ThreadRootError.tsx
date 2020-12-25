import React from "react"
import { ApolloError } from "apollo-client"
import RootError from "../../../UI/RootError"
import { ThreadValidationError } from "../../../UI/ValidationError"
import { MutationError } from "../../../types"

interface ThreadRootError {
  message: React.ReactNode
  type: string
}

interface ThreadRootErrorProps {
  children: (error: ThreadRootError) => React.ReactElement
  dataErrors?: Array<MutationError> | null
  graphqlError?: ApolloError | null
}

const ThreadRootError: React.FC<ThreadRootErrorProps> = ({
  children,
  dataErrors,
  graphqlError,
}) => (
  <RootError
    graphqlError={graphqlError}
    dataErrors={dataErrors}
    locations={["__root__", "thread"]}
  >
    {(error) => (
      <ThreadValidationError error={error}>{children}</ThreadValidationError>
    )}
  </RootError>
)

export default ThreadRootError
