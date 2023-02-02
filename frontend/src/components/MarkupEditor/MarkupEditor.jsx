import React from "react"
import classnames from "classnames"

import misago from "../../"
import ajax from "../../services/ajax"
import snackbar from "../../services/snackbar"
import MisagoMarkup from "../misago-markup"
import MarkupEditorFooter from "./MarkupEditorFooter"
import MarkupEditorToolbar from "./MarkupEditorToolbar"
import uploadFile from "./uploadFile"

class MarkupEditor extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      element: null,
      focused: false,
      loading: false,
      preview: false,
      parsed: null,
    }
  }

  showPreview = () => {
    if (this.state.loading) return

    this.setState({ loading: true, preview: true, element: null })

    ajax.post(misago.get("PARSE_MARKUP_API"), { post: this.props.value }).then(
      (data) => {
        this.setState({ loading: false, parsed: data.parsed })
      },
      (rejection) => {
        if (rejection.status === 400) {
          snackbar.error(rejection.detail)
        } else {
          snackbar.apiError(rejection)
        }

        this.setState({ loading: false })
      }
    )
  }

  closePreview = () => {
    this.setState({ preview: false })
  }

  onDrop = (event) => {
    event.preventDefault()
    event.stopPropagation()

    if (!event.dataTransfer.files) return

    const { onAttachmentsChange: setState } = this.props

    if (misago.get("user").acl.max_attachment_size) {
      for (let i = 0; i < event.dataTransfer.files.length; i++) {
        const file = event.dataTransfer.files[i]
        uploadFile(file, setState)
      }
    }
  }

  onPaste = (event) => {
    const { onAttachmentsChange: setState } = this.props

    const files = []
    for (let i = 0; i < event.clipboardData.items.length; i++) {
      const item = event.clipboardData.items[i]
      if (item.kind === "file") {
        files.push(item.getAsFile())
      }
    }

    if (files.length) {
      event.preventDefault()
      event.stopPropagation()

      if (misago.get("user").acl.max_attachment_size) {
        for (let i = 0; i < files.length; i++) {
          uploadFile(files[i], setState)
        }
      }
    }
  }

  render = () => (
    <div
      className={classnames("markup-editor", {
        "markup-editor-focused": this.state.focused && !this.state.preview,
      })}
    >
      <MarkupEditorToolbar
        disabled={this.props.disabled || this.state.preview}
        element={this.state.element}
        update={(value) => this.props.onChange({ target: { value } })}
        updateAttachments={this.props.onAttachmentsChange}
      />
      {this.state.preview ? (
        <div className="markup-editor-preview">
          {this.state.loading ? (
            "loading..."
          ) : (
            <MisagoMarkup markup={this.state.parsed} />
          )}
        </div>
      ) : (
        <textarea
          className="markup-editor-textarea form-control"
          placeholder={this.props.placeholder}
          value={this.props.value}
          disabled={this.props.disabled || this.state.loading}
          rows={6}
          ref={(element) => {
            if (element && !this.state.element) {
              this.setState({ element })
            }
          }}
          onChange={this.props.onChange}
          onDrop={this.onDrop}
          onFocus={() => this.setState({ focused: true })}
          onPaste={this.onPaste}
          onBlur={() => this.setState({ focused: false })}
        />
      )}
      {this.props.attachments.map((attachment) => (
        <div key={attachment.key}>
          {attachment.filename}
          {attachment.progress + "%"}
        </div>
      ))}
      <MarkupEditorFooter
        preview={this.state.preview}
        disabled={this.props.disabled}
        empty={
          this.props.value.trim().length <
            misago.get("SETTINGS").post_length_min || this.state.loading
        }
        showPreview={this.showPreview}
        closePreview={this.closePreview}
        submitText={this.props.submitText}
      />
    </div>
  )
}

export default MarkupEditor
