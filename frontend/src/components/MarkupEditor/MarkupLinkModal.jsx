import React from "react"
import modal from "../../services/modal"
import FormGroup from "../form-group"
import isUrl from "./isUrl"
import { replaceSelection } from "./operations"

class MarkupLinkModal extends React.Component {
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
      replaceSelection(selection, update, "[" + text + "](" + url + ")")
    } else {
      replaceSelection(selection, update, "<" + url + ">")
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
            <h4 className="modal-title">{pgettext("markup editor", "Link")}</h4>
          </div>
          <form onSubmit={this.handleSubmit}>
            <div className="modal-body">
              <FormGroup
                for="markup_link_url"
                label={pgettext("markup editor", "Link text")}
                helpText={pgettext(
                  "markup editor",
                  "Optional. Will be displayed instead of link's address."
                )}
              >
                <input
                  id="markup_link_text"
                  className="form-control"
                  type="text"
                  value={this.state.text}
                  onChange={(event) =>
                    this.setState({ text: event.target.value })
                  }
                />
              </FormGroup>
              <FormGroup
                for="markup_link_url"
                label={pgettext("markup editor", "Link address")}
                validation={!!this.state.error ? [this.state.error] : undefined}
              >
                <input
                  id="markup_link_url"
                  className="form-control"
                  type="text"
                  value={this.state.url}
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
                {pgettext("markup editor", "Insert link")}
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  }
}

export default MarkupLinkModal
