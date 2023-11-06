import React from "react"
import modal from "../../services/modal"
import FormGroup from "../form-group"
import isUrl from "./isUrl"
import { replaceSelection } from "./operations"

class MarkupImageModal extends React.Component {
  constructor(props) {
    super(props)

    const text = props.selection.text.trim()
    const textUrl = isUrl(text)

    this.state = {
      error: null,
      text: textUrl ? "" : text,
      url: textUrl ? text : "",
    }
  }

  handleSubmit = (ev) => {
    ev.preventDefault()

    const { selection, update } = this.props
    const text = this.state.text.trim()
    const url = this.state.url.trim()

    if (url.length === 0) {
      this.setState({ error: gettext("This field is required.") })
      return false
    }

    if (text.length > 0) {
      replaceSelection(selection, update, "![" + text + "](" + url + ")")
    } else {
      replaceSelection(selection, update, "!(" + url + ")")
    }

    modal.hide()

    return false
  }

  render() {
    return (
      <div className="modal-dialog" role="document">
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
              {pgettext("markup editor", "Image")}
            </h4>
          </div>
          <form onSubmit={this.handleSubmit}>
            <div className="modal-body">
              <FormGroup
                for="markup_image_text"
                label={pgettext("markup editor", "Image description")}
                helpText={pgettext(
                  "markup editor",
                  "Optional but recommended . Will be displayed instead of image when it fails to load."
                )}
              >
                <input
                  id="markup_image_text"
                  className="form-control"
                  type="text"
                  value={this.state.text}
                  onChange={(event) =>
                    this.setState({ text: event.target.value })
                  }
                />
              </FormGroup>
              <FormGroup
                for="markup_image_url"
                label={pgettext("markup editor", "Image URL")}
                validation={!!this.state.error ? [this.state.error] : undefined}
              >
                <input
                  id="markup_image_url"
                  className="form-control"
                  type="text"
                  value={this.state.url}
                  placeholder="http://domain.com/image.png"
                  onChange={(event) =>
                    this.setState({ url: event.target.value })
                  }
                />
              </FormGroup>
            </div>
            <div className="modal-footer">
              <button
                className="btn btn-default"
                data-dismiss="modal"
                type="button"
              >
                {pgettext("markup editor", "Cancel")}
              </button>
              <button className="btn btn-primary">
                {pgettext("markup editor", "Insert image")}
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  }
}

export default MarkupImageModal
