import React from "react"
import Button from "../button"

const MarkupEditorFooter = ({
  disabled,
  empty,
  preview,
  submitText,
  showPreview,
  closePreview,
}) => (
  <div className="markup-editor-footer">
    <div className="markup-editor-spacer" />
    {preview ? (
      <Button className="btn-default" onClick={closePreview} type="button">
        {pgettext("markup editor", "Edit")}
      </Button>
    ) : (
      <Button
        className="btn-default"
        disabled={disabled || empty}
        onClick={showPreview}
        type="button"
      >
        {pgettext("markup editor", "Preview")}
      </Button>
    )}
    <Button className="btn-primary" disabled={disabled || empty}>
      {submitText || gettext("Post")}
    </Button>
  </div>
)

export default MarkupEditorFooter
