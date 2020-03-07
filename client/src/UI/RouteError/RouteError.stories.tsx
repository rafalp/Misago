import React from "react"
import RouteError from "./RouteError"
import RouteNotFound from "./RouteNotFound"

export default {
  title: "Route/Error",
}

export const Error = () => <RouteError />

export const NotFound = () => <RouteNotFound />
