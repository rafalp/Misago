import { ApolloError } from "apollo-client"
import React from "react"
import { SettingsContextFactory } from "../Storybook"
import RouteAuthRequiredError from "./RouteAuthRequiredError"
import RouteError from "./RouteError"
import RouteGraphQLError from "./RouteGraphQLError"
import RouteNotFound from "./RouteNotFound"
import RoutePermissionDeniedError from "./RoutePermissionDeniedError"

export default {
  title: "Route/Error",
}

export const Default = () => (
  <SettingsContextFactory>
    <RouteError />
  </SettingsContextFactory>
)

export const NotFound = () => (
  <SettingsContextFactory>
    <RouteNotFound />
  </SettingsContextFactory>
)

export const AuthRequired = () => (
  <SettingsContextFactory>
    <RouteAuthRequiredError />
  </SettingsContextFactory>
)

export const PermissionDenied = () => (
  <SettingsContextFactory>
    <RoutePermissionDeniedError />
  </SettingsContextFactory>
)

export const QueryError = () => (
  <SettingsContextFactory>
    <RouteGraphQLError error={new ApolloError({})} />
  </SettingsContextFactory>
)

export const NetworkError = () => (
  <SettingsContextFactory>
    <RouteGraphQLError
      error={new ApolloError({ networkError: new Error() })}
    />
  </SettingsContextFactory>
)
