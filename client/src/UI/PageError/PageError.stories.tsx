import React from "react"
import PageError from "./PageError"
import PageNotFound from "./PageNotFound"

export default {
  title: "Pages/Error",
}

export const Error = () => <PageError />

export const NotFound = () => <PageNotFound />
