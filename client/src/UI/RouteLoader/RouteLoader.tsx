import React from "react"
import RouteContainer from "../RouteContainer"
import WindowTitle from "../WindowTitle"
import RouteLoaderSpinner from "./RouteLoaderSpinner"

const RouteLoader: React.FC = () => (
  <RouteContainer className="route-loader-container">
    <WindowTitle />
    <div className="container-fluid">
      <RouteLoaderSpinner />
    </div>
  </RouteContainer>
)

export default RouteLoader
