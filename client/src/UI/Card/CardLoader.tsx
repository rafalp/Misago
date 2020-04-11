import React from "react"
import Spinner from "../Spinner"

const CardLoader: React.FC = () => (
  <div className="card-body card-loader">
    <div className="card-loader-body">
      <Spinner />
    </div>
  </div>
)

export default CardLoader