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
)

export default MarkupEditorAttachments
