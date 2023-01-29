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
    <Button
      className="btn-default"
      disabled={disabled || empty}
      onClick={preview ? closePreview : showPreview}
      type="button"
    >
      {preview ? gettext("Edit") : gettext("Preview")}
    </Button>
    <Button className="btn-primary" loading={disabled} disabled={empty}>
      {submitText || gettext("Post")}
    </Button>
  </div>
)

export default MarkupEditorFooter
