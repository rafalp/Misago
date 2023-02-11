import React from "react"
import MarkupEditorAttachment from "./MarkupEditorAttachment"

const MarkupEditorAttachments = ({ attachments, disabled, setState }) => (
  <div className="markup-editor-attachments">
    {attachments.map((attachment) => (
      <MarkupEditorAttachment
        key={attachment.key || attachment.id}
        attachment={attachment}
        disabled={disabled}
        setState={setState}
      />
    ))}
  </div>
)

export default MarkupEditorAttachments
