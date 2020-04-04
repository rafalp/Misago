import classNames from "classnames"
import React from "react"
import { Error } from "../Error"
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
    <Error className="route" header={header} message={message} />
  </RouteContainer>
)

export default RouteError
