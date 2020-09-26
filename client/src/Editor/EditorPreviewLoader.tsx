import React from "react"
import Spinner from "../UI/Spinner"

const EditorPreviewLoader: React.FC = () => (
  <div className="form-editor-preview form-editor-preview-loader">
    <div className="form-editor-preview-loader-body">
      <Spinner />
    </div>
  </div>
)

export default EditorPreviewLoader
