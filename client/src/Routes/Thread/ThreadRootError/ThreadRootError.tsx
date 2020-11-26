import React from "react"
import { ApolloError } from "apollo-client"
import RootError from "../../../UI/RootError"
import { ThreadValidationError } from "../../../UI/ValidationError"
import { IMutationError } from "../../../types"

interface IThreadRootError {
  message: React.ReactNode
  type: string
}

interface IThreadRootErrorProps {
  children: (error: IThreadRootError) => React.ReactElement
  dataErrors?: Array<IMutationError> | null
  graphqlError?: ApolloError | null
}

const ThreadRootError: React.FC<IThreadRootErrorProps> = ({
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
