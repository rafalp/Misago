import classNames from "classnames"
import React from "react"
import { Error } from "../Error"
import RouteContainer from "../RouteContainer"
import WindowTitle from "../WindowTitle"

interface IRoutePermissionDeniedErrorProps {
  className?: string | null
  header?: React.ReactNode
  message?: React.ReactNode
  action?: React.ReactNode
}

const RoutePermissionDeniedError: React.FC<IRoutePermissionDeniedErrorProps> = ({
  className,
  header,
  message,
  action,
}) => (
  <RouteContainer
    className={classNames("route-permission-denied-container", className)}
  >
    <WindowTitle />
    <Error
      className="route"
      header={header}
      message={message}
      action={action}
    />
  </RouteContainer>
)

export default RoutePermissionDeniedError
