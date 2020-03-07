import React from "react"
import RouteContainer from "../RouteContainer"
import Spinner from "../Spinner"
import WindowTitle from "../WindowTitle"

const RouteLoader: React.FC = () => (
  <RouteContainer className="route-loader-container">
    <WindowTitle />
    <div className="container-fluid">
      <div className="route-loader">
        <div className="route-loader-body">
          <Spinner />
        </div>
      </div>
    </div>
  </RouteContainer>
)

export default RouteLoader
