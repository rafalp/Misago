import { Trans } from "@lingui/macro"
import React from "react"
import { ApolloError } from "apollo-client"
import { RouteError } from "../RouteError"
import getNetworkErrorCode from "../getNetworkErrorCode"

interface IRouteGraphQLError {
  error: ApolloError
}

const RouteGraphQLError: React.FC<IRouteGraphQLError> = ({ error }) => {
  const code = getNetworkErrorCode(error)
  if (error.networkError && code !== 400) {
    return (
      <RouteError
        className="route-offline-error-container"
        header={
          <Trans id="route_offline.title">
            Requested page could not be loaded.
          </Trans>
        }
        message={
          <Trans id="route_offline.message">
            Site server can't be reached. You may be offline or the site
            is unavailable at the moment.
          </Trans>
        }
      />
    )
  }

  return <RouteError />
}

export default RouteGraphQLError
