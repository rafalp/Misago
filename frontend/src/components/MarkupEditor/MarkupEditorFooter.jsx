import React from "react"
import Button from "../button"

const MarkupEditorFooter = ({
  canProtect,
  disabled,
  empty,
  preview,
  isProtected,
  submitText,
  showPreview,
  closePreview,
  enableProtection,
  disableProtection,
}) => (
  <div className="markup-editor-footer">
    {!!canProtect && (
      <Button
        className="btn-default btn-icon hidden-sm hidden-md hidden-lg"
        title={
          isProtected
            ? pgettext("markup editor", "Protected")
            : pgettext("markup editor", "Protect")
        }
        type="button"
        disabled={disabled}
        onClick={() => {
          if (isProtected) {
            disableProtection()
          } else {
            enableProtection()
          }
        }}
      >
        <span className="material-icon">
          {isProtected ? "lock" : "lock_open"}
        </span>
      </Button>
    )}
    {!!canProtect && (
      <div>
        <Button
          className="btn-default hidden-xs"
          type="button"
          disabled={disabled}
          onClick={() => {
            if (isProtected) {
              disableProtection()
            } else {
              enableProtection()
            }
          }}
        >
          <span className="material-icon">
            {isProtected ? "lock" : "lock_open"}
          </span>
          {isProtected
            ? pgettext("markup editor", "Protected")
            : pgettext("markup editor", "Protect")}
        </Button>
      </div>
    )}
    <div className="markup-editor-spacer" />
    {preview ? (
      <Button
        className="btn-default btn-auto"
        type="button"
        onClick={closePreview}
      >
        {pgettext("markup editor", "Edit")}
      </Button>
    ) : (
      <Button
        className="btn-default btn-auto"
        disabled={disabled || empty}
        type="button"
        onClick={showPreview}
      >
        {pgettext("markup editor", "Preview")}
      </Button>
    )}
    <Button className="btn-primary btn-auto" disabled={disabled || empty}>
      {submitText || pgettext("markup editor", "Post")}
    </Button>
  </div>
)

export default MarkupEditorFooter
