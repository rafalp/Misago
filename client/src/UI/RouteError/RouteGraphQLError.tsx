import { ApolloError } from "apollo-client"
import classNames from "classnames"
import React from "react"
import { GraphQLError } from "../Error"
import RouteContainer from "../RouteContainer"
import WindowTitle from "../WindowTitle"

interface IRouteGraphQLErrorProps {
  className?: string | null
  error: ApolloError
}

const RouteGraphQLError: React.FC<IRouteGraphQLErrorProps> = ({
  className,
  error,
}) => (
  <RouteContainer
    className={classNames("route-api-error-container", className)}
  >
    <WindowTitle />
    <GraphQLError className="route" error={error} />
  </RouteContainer>
)

export default RouteGraphQLError
