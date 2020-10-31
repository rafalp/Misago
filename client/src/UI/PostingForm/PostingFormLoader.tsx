import React from "react"
import Spinner from "../Spinner"

const PostingFormLoader: React.FC = () => (
  <div className="posting-form-loader">
    <div className="posting-form-loader-body">
      <Spinner />
    </div>
  </div>
)

export default PostingFormLoader
