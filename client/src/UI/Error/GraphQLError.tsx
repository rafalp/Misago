import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import GraphQLErrorRenderer from "../GraphQLErrorRenderer"
import Error from "./Error"
import GraphQLErrorMessage from "./GraphQLErrorMessage"

interface GrapQLErrorProps {
  className: string
  error: ApolloError
}

const GraphQLError: React.FC<GrapQLErrorProps> = ({ className, error }) => (
  <GraphQLErrorRenderer
    error={error}
    networkError={
      <Error
        className={className}
        header={
          <Trans id="api_error.title">
            Requested page could not be loaded.
          </Trans>
        }
        message={<GraphQLErrorMessage />}
      />
    }
    queryError={<Error className={className} />}
  />
)

export default GraphQLError
