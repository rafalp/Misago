import { Trans } from "@lingui/macro"
import classNames from "classnames"
import React from "react"
import RouteContainer from "../RouteContainer"
import WindowTitle from "../WindowTitle"

interface IRouteErrorProps {
  className?: string | null
  header?: React.ReactNode | null
  message?: React.ReactNode | null
}

const RouteError: React.FC<IRouteErrorProps> = ({
  className,
  header,
  message,
}) => (
  <RouteContainer className={classNames("route-error-container", className)}>
    <WindowTitle />
    <div className="route-error">
      <div className="route-error-body">
        <div className="route-error-icon" />
        <div className="route-error-message">
          <h1>
            {header || (
              <Trans id="route_error.title">
                Requested page could not be displayed due to an error.
              </Trans>
            )}
          </h1>
          <p>
            {message || (
              <Trans id="route_error.message">
                An unexpected error has occurred during displaying of this
                page.
              </Trans>
            )}
          </p>
        </div>
      </div>
    </div>
  </RouteContainer>
)

export default RouteError
