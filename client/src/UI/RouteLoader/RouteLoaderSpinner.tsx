import React from "react"
import Spinner from "../Spinner"

const RouteLoaderSpinner: React.FC = () => (
  <div className="route-loader">
    <div className="route-loader-body">
      <Spinner />
    </div>
  </div>
)

export default RouteLoaderSpinner
