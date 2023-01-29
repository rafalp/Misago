import React from "react"
import classnames from "classnames"

import ajax from "../../services/ajax"
import snackbar from "../../services/snackbar"
import MisagoMarkup from "../misago-markup"
import MarkupEditorFooter from "./MarkupEditorFooter"
import MarkupEditorToolbar from "./MarkupEditorToolbar"

// attachments={this.state.attachments}
// loading={this.state.isLoading}
// onAttachmentsChange={this.onAttachmentsChange}
// onCancel={this.onCancel}
// onChange={this.onPostChange}
// submitLabel={gettext("Post reply")}
// value={this.state.post}

class MarkupEditor extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      focused: false,
      loading: false,
      preview: false,
      parsed: null,
    }
  }

  showPreview = () => {
    if (this.state.loading) return

    this.setState({ loading: true, preview: true })

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

  render = () => (
    <div
      className={classnames("markup-editor", {
        "markup-editor-focused": this.state.focused && !this.state.preview,
      })}
    >
      <MarkupEditorToolbar />
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
          value={this.props.value}
          disabled={this.props.disabled || this.state.loading}
          onChange={this.props.onChange}
          onFocus={() => this.setState({ focused: true })}
          onBlur={() => this.setState({ focused: false })}
        />
      )}
      <MarkupEditorFooter
        preview={this.state.preview}
        disabled={this.props.disabled}
        empty={this.props.value.trim().length === 0 || this.state.loading}
        showPreview={this.showPreview}
        closePreview={this.closePreview}
        submitText={this.props.submitText}
      />
    </div>
  )
}

export default MarkupEditor
