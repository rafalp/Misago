import classnames from "classnames"
import React from "react"
import { Error } from "../Error"
import RouteContainer from "../RouteContainer"
import WindowTitle from "../WindowTitle"

interface IRouteErrorProps {
  className?: string | null
  header?: React.ReactNode
  message?: React.ReactNode
  action?: React.ReactNode
}

const RouteError: React.FC<IRouteErrorProps> = ({
  className,
  header,
  message,
  action,
}) => (
  <RouteContainer className={classnames("route-error-container", className)}>
    <WindowTitle />
    <Error
      className="route"
      header={header}
      message={message}
      action={action}
    />
  </RouteContainer>
)

export default RouteError
