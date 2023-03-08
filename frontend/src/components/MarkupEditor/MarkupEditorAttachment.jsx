import React from "react"
import modal from "../../services/modal"
import snackbar from "../../services/snackbar"
import formatFilesize from "../../utils/file-size"
import MarkupAttachmentModal from "./MarkupAttachmentModal"
import { getSelection, replaceSelection } from "./operations"

const MarkupEditorAttachment = ({
  attachment,
  disabled,
  element,
  setState,
  update,
}) => (
  <div className="markup-editor-attachments-item">
    <div className="markup-editor-attachment">
      <div className="markup-editor-attachment-details">
        {attachment.id ? (
          <a
            className="item-title"
            href={attachment.url.index + "?shva=1"}
            target="_blank"
            onClick={(event) => {
              event.preventDefault()
              modal.show(<MarkupAttachmentModal attachment={attachment} />)
            }}
          >
            {attachment.filename}
          </a>
        ) : (
          <strong className="item-title">{attachment.filename}</strong>
        )}
        <div className="text-muted">
          <ul className="list-unstyled list-inline">
            {!attachment.id && <li>{attachment.progress + "%"}</li>}
            {!!attachment.filetype && <li>{attachment.filetype}</li>}
            {attachment.size > 0 && <li>{formatFilesize(attachment.size)}</li>}
          </ul>
        </div>
      </div>
      {!!attachment.id && (
        <div className="markup-editor-attachment-buttons">
          <button
            className="btn btn-markup-editor-attachment btn-icon"
            title={pgettext("markup editor", "Insert into message")}
            type="button"
            disabled={disabled}
            onClick={() => {
              const markup = getAttachmentMarkup(attachment)
              const selection = getSelection(element)
              replaceSelection(selection, update, markup)
            }}
          >
            <span className="material-icon">flip_to_front</span>
          </button>
          <button
            className="btn btn-markup-editor-attachment btn-icon"
            title={pgettext("markup editor", "Remove attachment")}
            type="button"
            disabled={disabled}
            onClick={() => {
              setState(({ attachments }) => {
                const confirm = window.confirm(
                  pgettext("markup editor", "Remove this attachment?")
                )

                if (confirm) {
                  return {
                    attachments: attachments.filter(
                      ({ id }) => id !== attachment.id
                    ),
                  }
                }
              })
            }}
          >
            <span className="material-icon">close</span>
          </button>
        </div>
      )}
      {!attachment.id && !!attachment.key && (
        <div className="markup-editor-attachment-buttons">
          {attachment.error && (
            <button
              className="btn btn-markup-editor-attachment btn-icon"
              title={pgettext("markup editor", "See error")}
              type="button"
              onClick={() => {
                snackbar.error(
                  interpolate(
                    pgettext("markup editor", "%(filename)s: %(error)s"),
                    { filename: attachment.filename, error: attachment.error },
                    true
                  )
                )
              }}
            >
              <span className="material-icon">warning</span>
            </button>
          )}
          <button
            className="btn btn-markup-editor-attachment btn-icon"
            title={pgettext("markup editor", "Remove attachment")}
            type="button"
            disabled={disabled}
            onClick={() => {
              setState(({ attachments }) => {
                return {
                  attachments: attachments.filter(
                    ({ key }) => key !== attachment.key
                  ),
                }
              })
            }}
          >
            <span className="material-icon">close</span>
          </button>
        </div>
      )}
    </div>
  </div>
)

export default MarkupEditorAttachment

function getAttachmentMarkup(attachment) {
  let markup = "["

  if (attachment.is_image) {
    markup += "![" + attachment.filename + "]"
    markup += "(" + (attachment.url.thumb || attachment.url.index) + "?shva=1)"
  } else {
    markup += attachment.filename
  }

  markup += "](" + attachment.url.index + "?shva=1)"
  return markup
}
