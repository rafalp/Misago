import React from "react"

const MarkupEditorButton = ({ disabled, icon, title, onClick }) => (
  <button
    className="btn btn-markup-editor"
    title={title}
    type="button"
    disabled={disabled}
    onClick={onClick}
  >
    <span className="material-icon">{icon}</span>
  </button>
)

export default MarkupEditorButton
