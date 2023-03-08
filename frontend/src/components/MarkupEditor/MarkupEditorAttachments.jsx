import React from "react"
import MarkupEditorAttachment from "./MarkupEditorAttachment"

const MarkupEditorAttachments = ({
  attachments,
  disabled,
  element,
  setState,
  update,
}) => (
  <div className="markup-editor-attachments">
    <div className="markup-editor-attachments-container">
      {attachments.map((attachment) => (
        <MarkupEditorAttachment
          key={attachment.key || attachment.id}
          attachment={attachment}
          disabled={disabled}
          element={element}
          setState={setState}
          update={update}
        />
      ))}
    </div>
  </div>
)

export default MarkupEditorAttachments
