import React from "react"
import Fieldset from "./fieldset"
import Button from "misago/components/button"
import Form from "misago/components/form"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,

      errors: {},
    }

    const groups = props.groups.length
    for (let i = 0; i < groups; i++) {
      const group = props.groups[i]
      const fields = group.fields.length
      for (let f = 0; f < fields; f++) {
        const fieldname = group.fields[f].fieldname
        const initial = group.fields[f].initial
        this.state[fieldname] = initial
      }
    }
  }

  send() {
    const data = Object.assign({}, this.state, {
      errors: null,
      isLoading: null,
    })

    return ajax.post(this.props.api, data)
  }

  handleSuccess(data) {
    this.props.onSuccess(data)
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      snackbar.error(gettext("Form contains errors."))
      this.setState({ errors: rejection })
    } else {
      snackbar.apiError(rejection)
    }
  }

  onChange = (name, value) => {
    this.setState({
      [name]: value,
    })
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="panel-body">
          {this.props.groups.map((group, i) => {
            return (
              <Fieldset
                disabled={this.state.isLoading}
                errors={this.state.errors}
                fields={group.fields}
                name={group.name}
                key={i}
                onChange={this.onChange}
                value={this.state}
              />
            )
          })}
        </div>
        <div className="panel-footer text-right">
          <CancelButton
            disabled={this.state.isLoading}
            onCancel={this.props.onCancel}
          />{" "}
          <Button className="btn-primary" loading={this.state.isLoading}>
            {pgettext("user profile details form btn", "Save changes")}
          </Button>
        </div>
      </form>
    )
  }
}

export function CancelButton({ onCancel, disabled }) {
  if (!onCancel) return null

  return (
    <button
      className="btn btn-default"
      disabled={disabled}
      onClick={onCancel}
      type="button"
    >
      {pgettext("user profile details form btn", "Cancel")}
    </button>
  )
}
