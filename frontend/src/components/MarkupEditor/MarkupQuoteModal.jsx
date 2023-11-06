import React from "react"
import modal from "../../services/modal"
import FormGroup from "../form-group"
import { replaceSelection } from "./operations"

class MarkupQuoteModal extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      error: null,
      author: "",
      text: props.selection.text,
    }
  }

  handleSubmit = (ev) => {
    ev.preventDefault()

    const { selection, update } = this.props
    const author = this.state.author.trim()
    const text = this.state.text.trim()

    if (text.length === 0) {
      this.setState({ error: gettext("This field is required.") })
      return false
    }

    const prefix = selection.prefix.trim().length ? "\n\n" : ""

    if (author) {
      replaceSelection(
        selection,
        update,
        prefix + '[quote="' + author + '"]\n' + text + "\n[/quote]\n\n"
      )
    } else {
      replaceSelection(
        selection,
        update,
        prefix + "[quote]\n" + text + "\n[/quote]\n\n"
      )
    }

    modal.hide()

    return false
  }

  render() {
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
              {pgettext("markup editor", "Quote")}
            </h4>
          </div>
          <form onSubmit={this.handleSubmit}>
            <div className="modal-body">
              <FormGroup
                for="markup_quote_author"
                label={pgettext("markup editor", "Quote's author or source")}
                helpText={pgettext(
                  "markup editor",
                  'Optional. If it\'s username, put "@" before it ("@JohnDoe").'
                )}
              >
                <input
                  id="markup_quote_author"
                  className="form-control"
                  type="text"
                  value={this.state.author}
                  onChange={(event) =>
                    this.setState({ author: event.target.value })
                  }
                />
              </FormGroup>
              <FormGroup
                for="markup_quote_text"
                label={pgettext("markup editor", "Quoted text")}
                validation={!!this.state.error ? [this.state.error] : undefined}
              >
                <textarea
                  id="markup_quote_text"
                  className="form-control"
                  rows="8"
                  value={this.state.text}
                  onChange={(event) =>
                    this.setState({ text: event.target.value })
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
                {pgettext("markup editor", "Insert quote")}
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  }
}

export default MarkupQuoteModal
