import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import { CardError } from "../../../UI/Card"
import { ErrorMessage, GraphQLErrorMessage } from "../../../UI/Error"
import GraphQLErrorRenderer from "../../../UI/GraphQLErrorRenderer"

interface ThreadsListGraphQLErrorProps {
  error: ApolloError
}

const ThreadsListGraphQLError: React.FC<ThreadsListGraphQLErrorProps> = ({
  error,
}) => (
  <GraphQLErrorRenderer
    error={error}
    networkError={
      <CardError header={<ErrorHeader />} message={<GraphQLErrorMessage />} />
    }
    queryError={
      <CardError header={<ErrorHeader />} message={<ErrorMessage />} />
    }
  />
)

const ErrorHeader: React.FC = () => (
  <Trans id="threads.graphql_error_header">
    Threads list could not be displayed.
  </Trans>
)

export default ThreadsListGraphQLError
