import React from "react"
import Spinner from "../../../UI/Spinner"

const ThreadPostLoader: React.FC = () => (
  <div className="card-body post-loader">
    <div className="post-loader-body">
      <Spinner />
    </div>
  </div>
)

export default ThreadPostLoader
