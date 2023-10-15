import React from "react"
import modal from "../../services/modal"
import FormGroup from "../form-group"
import { replaceSelection } from "./operations"

class MarkupCodeModal extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      error: null,
      syntax: "",
      text: props.selection.text,
    }
  }

  handleSubmit = (ev) => {
    ev.preventDefault()

    const { selection, update } = this.props
    const syntax = this.state.syntax.trim()
    const text = this.state.text.trim()

    if (text.length === 0) {
      this.setState({ error: gettext("This field is required.") })
      return false
    }

    const prefix = selection.prefix.trim().length ? "\n\n" : ""

    replaceSelection(
      Object.assign({}, selection, { text }),
      update,
      prefix + "```" + syntax + "\n" + text + "\n```\n\n"
    )

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
            <h4 className="modal-title">{pgettext("markup editor", "Code")}</h4>
          </div>
          <form onSubmit={this.handleSubmit}>
            <div className="modal-body">
              <FormGroup
                for="markup_code_syntax"
                label={pgettext("markup editor", "Syntax highlighting")}
              >
                <select
                  id="markup_code_syntax"
                  className="form-control"
                  value={this.state.syntax}
                  onChange={(event) =>
                    this.setState({ syntax: event.target.value })
                  }
                >
                  <option value="">
                    {pgettext("markup editor", "No syntax highlighting")}
                  </option>
                  {LANGUAGES.map(({ value, name }) => (
                    <option key={value} value={value}>
                      {name}
                    </option>
                  ))}
                </select>
              </FormGroup>
              <FormGroup
                for="markup_code_text"
                label={pgettext("markup editor", "Code to insert")}
                validation={!!this.state.error ? [this.state.error] : undefined}
              >
                <textarea
                  id="markup_code_text"
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
                {pgettext("markup editor", "Insert code")}
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  }
}

const LANGUAGES = [
  { value: "bash", name: "Bash" },
  { value: "c", name: "C" },
  { value: "c#", name: "C#" },
  { value: "c++", name: "C++" },
  { value: "css", name: "CSS" },
  { value: "diff", name: "Diff" },
  { value: "go", name: "Go" },
  { value: "graphql", name: "GraphQL" },
  { value: "html,", name: "HTML" },
  { value: "xml", name: "XML" },
  { value: "json", name: "JSON" },
  { value: "java", name: "Java" },
  { value: "javascript", name: "JavaScript" },
  { value: "kotlin", name: "Kotlin" },
  { value: "less", name: "Less" },
  { value: "lua", name: "Lua" },
  { value: "makefile", name: "Makefile" },
  { value: "markdown", name: "Markdown" },
  { value: "objective-C", name: "Objective-C" },
  { value: "php", name: "PHP" },
  { value: "perl", name: "Perl" },
  { value: "plain", name: "Plain" },
  { value: "text", name: "text" },
  { value: "python", name: "Python" },
  { value: "repl", name: "REPL" },
  { value: "r", name: "R" },
  { value: "ruby", name: "Ruby" },
  { value: "rust", name: "Rust" },
  { value: "scss", name: "SCSS" },
  { value: "sql", name: "SQL" },
  { value: "shell", name: "Shell Session" },
  { value: "swift", name: "Swift" },
  { value: "toml", name: "TOML" },
  { value: "ini", name: "INI" },
  { value: "typescript", name: "TypeScript" },
  { value: "visualbasic", name: "Visual Basic .NET" },
  { value: "webassembly", name: "WebAssembly" },
  { value: "yaml", name: "YAML" },
]

export default MarkupCodeModal
