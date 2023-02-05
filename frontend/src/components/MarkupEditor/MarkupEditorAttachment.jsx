import React from "react"

const MarkupEditorAttachment = ({ attachment, disabled, setState }) => (
  <div className="markup-editor-attachments-item">
    <div className="markup-editor-attachment">
      <div className="markup-editor-attachment-details">
        {attachment.id ? (
          <a
            className="item-title"
            href={attachment.url.index + "?shva=1"}
            target="_blank"
          >
            {attachment.filename}
          </a>
        ) : (
          <strong className="item-title">{attachment.filename}</strong>
        )}
        <div className="text-muted">{attachment.size}</div>
      </div>
      <div className="markup-editor-attachment-buttons">
        {!!attachment.id && (
          <button
            className="btn btn-markup-editor-attachment"
            type="button"
            disabled={disabled}
            onClick={() => {
              setState(({ attachments }) => {
                return {
                  attachments: attachments.filter(
                    ({ id }) => id !== attachment.id
                  ),
                }
              })
            }}
          >
            <span className="material-icon">close</span>
          </button>
        )}
        {!attachment.id && (
          <button className="btn btn-markup-editor-attachment" disabled>
            {attachment.progress + "%"}
          </button>
        )}
      </div>
    </div>
  </div>
)

export default MarkupEditorAttachment
