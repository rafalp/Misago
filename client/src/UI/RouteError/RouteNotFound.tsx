import { Trans } from "@lingui/macro"
import React from "react"
import PageError from "./RouteError"

interface IRouteNotFoundProps {
  header?: React.ReactNode | null
  message?: React.ReactNode | null
}

const RouteNotFound: React.FC<IRouteNotFoundProps> = ({ header, message }) => (
  <PageError
    className="route-not-found-container"
    header={
      header || (
        <Trans id="route_not_found.title">
          Requested page could not be found.
        </Trans>
      )
    }
    message={
      message || (
        <Trans id="route_not_found.message">
          The link you followed was incorrect or the page has been moved or
          deleted.
        </Trans>
      )
    }
  />
)

export default RouteNotFound
