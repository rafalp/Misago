import React from "react"

interface IEditorToolbarProps {
  children: React.ReactNode
}

const EditorToolbar: React.FC<IEditorToolbarProps> = ({ children }) => (
  <div className="form-editor-toolbar">{children}</div>
)

export default EditorToolbar
