import React from "react"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import { getTitleValidators } from "misago/components/posting/utils/validators"
import * as thread from "misago/reducers/thread"
import ajax from "misago/services/ajax"
import modal from "misago/services/modal"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,

      title: props.thread.title,

      validators: {
        title: getTitleValidators(),
      },
      errors: {},
    }
  }

  clean() {
    if (!this.state.title.trim().length) {
      snackbar.error(
        pgettext("thread title form", "You have to enter thread title.")
      )
      return false
    }

    const errors = this.validate()

    if (errors.title) {
      snackbar.error(errors.title[0])
      return false
    }

    return true
  }

  send() {
    // freeze thread
    store.dispatch(thread.busy())

    return ajax.patch(this.props.thread.api.index, [
      { op: "replace", path: "title", value: this.state.title },
    ])
  }

  handleSuccess = (data) => {
    this.handleSuccessUnmounted(data)

    // keep form loading
    this.setState({
      isLoading: true,
    })

    modal.hide()
  }

  handleSuccessUnmounted = (data) => {
    store.dispatch(thread.release())
    store.dispatch(thread.update(data))
  }

  handleError = (rejection) => {
    store.dispatch(thread.release())

    if (rejection.status === 400) {
      snackbar.error(rejection.detail[0])
    } else {
      snackbar.apiError(rejection)
    }
  }

  onChange = (event) => {
    this.changeValue("title", event.target.value)
  }

  render() {
    return (
      <div className="modal-dialog modal-lg" role="document">
        <form onSubmit={this.handleSubmit}>
          <div className="modal-content">
            <ModalHeader />
            <div className="modal-body">
              <FormGroup
                for="id_modal_title"
                label={pgettext("thread title form field", "Thread title")}
              >
                <input
                  className="form-control"
                  disabled={this.state.isLoading || this.props.thread.isBusy}
                  id="id_modal_title"
                  onChange={this.onChange}
                  value={this.state.title}
                />
              </FormGroup>
            </div>
            <div className="modal-footer">
              <button
                className="btn btn-default"
                data-dismiss="modal"
                disabled={this.state.isLoading}
                type="button"
              >
                {pgettext("thread title form btn", "Cancel")}
              </button>
              <button
                className="btn btn-primary"
                disabled={this.state.isLoading || this.props.thread.isBusy}
              >
                {pgettext("thread title form btn", "Change title")}
              </button>
            </div>
          </div>
        </form>
      </div>
    )
  }
}

export function ModalHeader(props) {
  return (
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
        {pgettext("thread title form title", "Change title")}
      </h4>
    </div>
  )
}
