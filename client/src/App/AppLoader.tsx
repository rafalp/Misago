import React from "react"
import Spinner from "../UI/Spinner"

const AppLoader = () => (
  <div className="app-loader">
    <div className="app-loader-body">
      <Spinner />
    </div>
  </div>
)

export default AppLoader
