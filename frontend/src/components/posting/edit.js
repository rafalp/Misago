import React from "react"
import Editor from "misago/components/editor"
import Form from "misago/components/form"
import Container from "./utils/container"
import Loader from "./utils/loader"
import Message from "./utils/message"
import * as attachments from "./utils/attachments"
import { getPostValidators } from "./utils/validators"
import ajax from "misago/services/ajax"
import posting from "misago/services/posting"
import snackbar from "misago/services/snackbar"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isReady: false,
      isLoading: false,
      isErrored: false,

      post: "",
      attachments: [],
      protect: false,

      canProtect: false,

      validators: {
        post: getPostValidators(),
      },
      errors: {},
    }
  }

  componentDidMount() {
    ajax.get(this.props.config).then(this.loadSuccess, this.loadError)
  }

  loadSuccess = (data) => {
    this.setState({
      isReady: true,

      post: data.post,
      attachments: attachments.hydrate(data.attachments),
      protect: data.is_protected,

      canProtect: data.can_protect,
    })
  }

  loadError = (rejection) => {
    this.setState({
      isErrored: rejection.detail,
    })
  }

  onCancel = () => {
    const cancel = window.confirm(
      gettext("Are you sure you want to discard changes?")
    )
    if (cancel) {
      posting.close()
    }
  }

  onProtect = () => {
    this.setState({
      protect: true,
    })
  }

  onUnprotect = () => {
    this.setState({
      protect: false,
    })
  }

  onPostChange = (event) => {
    this.changeValue("post", event.target.value)
  }

  onAttachmentsChange = (attachments) => {
    this.setState({
      attachments,
    })
  }

  clean() {
    if (!this.state.post.trim().length) {
      snackbar.error(gettext("You have to enter a message."))
      return false
    }

    const errors = this.validate()

    if (errors.post) {
      snackbar.error(errors.post[0])
      return false
    }

    return true
  }

  send() {
    return ajax.put(this.props.submit, {
      post: this.state.post,
      attachments: attachments.clean(this.state.attachments),
      protect: this.state.protect,
    })
  }

  handleSuccess(success) {
    snackbar.success(gettext("Reply has been edited."))
    window.location = success.url.index

    // keep form loading
    this.setState({
      isLoading: true,
    })
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      const errors = [].concat(
        rejection.non_field_errors || [],
        rejection.category || [],
        rejection.title || [],
        rejection.post || [],
        rejection.attachments || []
      )

      snackbar.error(errors[0])
    } else {
      snackbar.apiError(rejection)
    }
  }

  render() {
    if (this.state.isReady) {
      return (
        <Container className="posting-form">
          <form onSubmit={this.handleSubmit} method="POST">
            <div className="row">
              <div className="col-md-12">
                <Editor
                  attachments={this.state.attachments}
                  canProtect={this.state.canProtect}
                  loading={this.state.isLoading}
                  onAttachmentsChange={this.onAttachmentsChange}
                  onCancel={this.onCancel}
                  onChange={this.onPostChange}
                  onProtect={this.onProtect}
                  onUnprotect={this.onUnprotect}
                  protect={this.state.protect}
                  submitLabel={gettext("Edit reply")}
                  value={this.state.post}
                />
              </div>
            </div>
          </form>
        </Container>
      )
    } else if (this.state.isErrored) {
      return <Message message={this.state.isErrored} />
    } else {
      return <Loader />
    }
  }
}
