import React from "react"
import AppError from "./AppError"
import AppLoader from "./AppLoader"

export default {
  title: "Pages/App",
}

export const Error = () => <AppError />
export const Loader = () => <AppLoader />
