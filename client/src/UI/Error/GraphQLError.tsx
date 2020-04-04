import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import Error from "./Error"
import getNetworkErrorCode from "../getNetworkErrorCode"

interface IGraphQLErrorProps {
  className: string
  error: ApolloError
}

const GraphQLError: React.FC<IGraphQLErrorProps> = ({
  className,
  error,
}) => {
  const code = getNetworkErrorCode(error)

  if (error.networkError && code !== 400) {
    return (
      <Error
        className={className}
        header={
          <Trans id="api_error.title">
            Requested page could not be loaded.
          </Trans>
        }
        message={
          <Trans id="api_error.message">
            Site server can't be reached. You may be offline or the site is
            unavailable at the moment.
          </Trans>
        }
      />
    )
  }

  return <Error className={className} />
}

export default GraphQLError
