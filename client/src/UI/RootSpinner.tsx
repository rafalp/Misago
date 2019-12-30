import React from "react"
import AppContainer from "./AppContainer"
import Spinner from "./Spinner"

const RootSpinner: React.FC = () => (
  <AppContainer>
    <div className="root-spinner">
      <Spinner />
    </div>
  </AppContainer>
)

export default RootSpinner
