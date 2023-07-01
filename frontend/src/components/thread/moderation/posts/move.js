import React from "react"
import Button from "misago/components/button"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import * as post from "misago/reducers/post"
import ajax from "misago/services/ajax"
import modal from "misago/services/modal"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,

      url: "",

      validators: {
        url: [],
      },
      errors: {},
    }
  }

  clean() {
    if (!this.state.url.trim().length) {
      snackbar.error(
        pgettext(
          "thread posts moderation move",
          "You have to enter link to the other thread."
        )
      )
      return false
    }

    return true
  }

  send() {
    return ajax.post(this.props.thread.api.posts.move, {
      new_thread: this.state.url,
      posts: this.props.selection.map((post) => post.id),
    })
  }

  handleSuccess(success) {
    this.props.selection.forEach((selection) => {
      store.dispatch(
        post.patch(selection, {
          isDeleted: true,
        })
      )
    })

    modal.hide()

    snackbar.success(
      pgettext(
        "thread posts moderation move",
        "Selected posts were moved to the other thread."
      )
    )
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      snackbar.error(rejection.detail)
    } else {
      snackbar.apiError(rejection)
    }
  }

  onUrlChange = (event) => {
    this.changeValue("url", event.target.value)
  }

  render() {
    return (
      <div className="modal-dialog" role="document">
        <form onSubmit={this.handleSubmit}>
          <div className="modal-content">
            <ModalHeader />
            <div className="modal-body">
              <FormGroup
                for="id_url"
                label={pgettext(
                  "thread posts moderation move",
                  "Link to thread you want to move posts to"
                )}
              >
                <input
                  className="form-control"
                  disabled={this.state.isLoading}
                  id="id_url"
                  onChange={this.onUrlChange}
                  value={this.state.url}
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
                {pgettext("thread posts moderation move btn", "Cancel")}
              </button>
              <button
                className="btn btn-primary"
                disabled={this.state.isLoading}
              >
                {pgettext("thread posts moderation move btn", "Move posts")}
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
        {pgettext("thread posts moderation move title", "Move posts")}
      </h4>
    </div>
  )
}
