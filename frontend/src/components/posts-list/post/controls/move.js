import React from "react"
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
          "post move modal",
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
      posts: [this.props.post.id],
    })
  }

  handleSuccess(success) {
    store.dispatch(
      post.patch(this.props.post, {
        isDeleted: true,
      })
    )

    modal.hide()

    snackbar.success(
      pgettext(
        "post move modal",
        "Selected post was moved to the other thread."
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
                  "post move modal field",
                  "Link to thread you want to move post to"
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
                className="btn btn-primary"
                disabled={this.state.isLoading}
              >
                {pgettext("post move modal btn", "Move post")}
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
        {pgettext("post move modal title", "Move post")}
      </h4>
    </div>
  )
}
