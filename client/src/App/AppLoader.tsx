import React from "react"
import { Spinner } from "../UI"

const AppLoader = () => (
  <div className="app-loader">
    <div className="app-loader-body">
      <Spinner />
    </div>
  </div>
)

export default AppLoader
