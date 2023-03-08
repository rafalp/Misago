import React from "react"
import formatFilesize from "../../utils/file-size"

export default function MarkupAttachmentModal({ attachment }) {
  return (
    <div className="modal-dialog modal-lg" role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button
            aria-label={pgettext("modal", "Close")}
            className="close"
            data-dismiss="modal"
            type="button"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">
            {pgettext("markup editor", "Attachment details")}
          </h4>
        </div>
        <div className="modal-body">
          {!!attachment.is_image && (
            <div className="markup-editor-attachment-modal-preview">
              <a href={attachment.url.index + "?shva=1"} target="_blank">
                <img src={attachment.url.index + "?shva=1"} alt="" />
              </a>
            </div>
          )}
          <div className="markup-editor-attachment-modal-filename">
            {attachment.filename}
          </div>
          <div className="row markup-editor-attachment-modal-details">
            <div className="col-xs-12 col-md-3">
              <strong>
                {attachment.filetype + ", " + formatFilesize(attachment.size)}
              </strong>
              <div className="text-muted">
                <small>{pgettext("markup editor", "Type and size")}</small>
              </div>
            </div>
            <div className="col-xs-12 col-md-4">
              <strong>
                <abbr title={attachment.uploaded_on.format("LLL")}>
                  {attachment.uploaded_on.fromNow()}
                </abbr>
              </strong>
              <div className="text-muted">
                <small>{pgettext("markup editor", "Uploaded at")}</small>
              </div>
            </div>
            <div className="col-xs-12 col-md-3">
              {attachment.url.uploader ? (
                <a
                  href={attachment.url.uploader}
                  target="_blank"
                  className="item-title"
                >
                  {attachment.uploader_name}
                </a>
              ) : (
                <span className="item-title">{attachment.uploader_name}</span>
              )}
              <div className="text-muted">
                <small>{pgettext("markup editor", "Uploader")}</small>
              </div>
            </div>
          </div>
        </div>
        <div className="modal-footer">
          <button
            className="btn btn-default"
            data-dismiss="modal"
            type="button"
          >
            {pgettext("modal", "Close")}
          </button>
        </div>
      </div>
    </div>
  )
}
