import classnames from "classnames"
import React from "react"
import { NotFoundError } from "../Error"
import RouteContainer from "../RouteContainer"
import WindowTitle from "../WindowTitle"

interface IRouteNotFoundProps {
  className?: string | null
  header?: React.ReactNode
  message?: React.ReactNode
}

const RouteNotFound: React.FC<IRouteNotFoundProps> = ({
  className,
  header,
  message,
}) => (
  <RouteContainer
    className={classnames("route-not-found-container", className)}
  >
    <WindowTitle />
    <NotFoundError className="route" header={header} message={message} />
  </RouteContainer>
)

export default RouteNotFound
