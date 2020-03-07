import React from "react"
import AppError from "./AppError"
import AppLoader from "./AppLoader"

export default {
  title: "App",
}

export const Error = () => <AppError />
export const Loader = () => <AppLoader />
