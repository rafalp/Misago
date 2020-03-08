import { ApolloError } from "apollo-client"
import React from "react"
import RouteGraphQLError from "./RouteGraphQLError"

export default {
  title: "Route/GraphQL Error",
}

export const QueryError = () => (
  <RouteGraphQLError error={new ApolloError({})} />
)

export const NetworkError = () => (
  <RouteGraphQLError error={new ApolloError({ networkError: new Error() })} />
)
