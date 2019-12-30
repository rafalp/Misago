import React from "react"
import RootContainer from "./RootContainer"
import Spinner from "./Spinner"

const RootSpinner: React.FC = () => (
  <RootContainer>
    <div className="root-spinner">
      <Spinner />
    </div>
  </RootContainer>
)

export default RootSpinner
