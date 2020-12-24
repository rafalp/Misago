import React from "react"

interface EditorToolbarProps {
  children: React.ReactNode
}

const EditorToolbar: React.FC<EditorToolbarProps> = ({ children }) => (
  <div className="form-editor-toolbar">{children}</div>
)

export default EditorToolbar
