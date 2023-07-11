import React from "react"
import Form from "misago/components/form"
import * as attachments from "./utils/attachments"
import cleanUsernames from "./utils/usernames"
import { getPostValidators, getTitleValidators } from "./utils/validators"
import ajax from "misago/services/ajax"
import posting from "misago/services/posting"
import snackbar from "misago/services/snackbar"
import MarkupEditor from "../MarkupEditor"
import { Toolbar, ToolbarItem, ToolbarSection } from "../Toolbar"
import PostingDialog from "./PostingDialog"
import PostingDialogBody from "./PostingDialogBody"
import PostingDialogHeader from "./PostingDialogHeader"

export default class extends Form {
  constructor(props) {
    super(props)

    const to = (props.to || []).map((user) => user.username).join(", ")

    this.state = {
      isLoading: false,

      error: null,

      minimized: false,
      fullscreen: false,

      to: to,
      title: "",
      post: "",
      attachments: [],

      validators: {
        title: getTitleValidators(),
        post: getPostValidators(),
      },
      errors: {},
    }
  }

  onCancel = () => {
    const formEmpty = !!(
      this.state.post.length === 0 &&
      this.state.title.length === 0 &&
      this.state.to.length === 0 &&
      this.state.attachments.length === 0
    )

    if (formEmpty) {
      return this.close()
    }

    const cancel = window.confirm(
      pgettext(
        "post thread",
        "Are you sure you want to discard private thread?"
      )
    )
    if (cancel) {
      this.close()
    }
  }

  onToChange = (event) => {
    this.changeValue("to", event.target.value)
  }

  onTitleChange = (event) => {
    this.changeValue("title", event.target.value)
  }

  onPostChange = (event) => {
    this.changeValue("post", event.target.value)
  }

  onAttachmentsChange = (attachments) => {
    this.setState(attachments)
  }

  clean() {
    if (!cleanUsernames(this.state.to).length) {
      snackbar.error(
        pgettext("posting form", "You have to enter at least one recipient.")
      )
      return false
    }

    if (!this.state.title.trim().length) {
      snackbar.error(
        pgettext("posting form", "You have to enter thread title.")
      )
      return false
    }

    if (!this.state.post.trim().length) {
      snackbar.error(pgettext("posting form", "You have to enter a message."))
      return false
    }

    const errors = this.validate()

    if (errors.title) {
      snackbar.error(errors.title[0])
      return false
    }

    if (errors.post) {
      snackbar.error(errors.post[0])
      return false
    }

    return true
  }

  send() {
    return ajax.post(this.props.submit, {
      to: cleanUsernames(this.state.to),
      title: this.state.title,
      post: this.state.post,
      attachments: attachments.clean(this.state.attachments),
    })
  }

  handleSuccess(success) {
    this.setState({ isLoading: true })
    this.close()

    snackbar.success(pgettext("post thread", "Your thread has been posted."))
    window.location = success.url
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      const errors = [].concat(
        rejection.non_field_errors || [],
        rejection.to || [],
        rejection.title || [],
        rejection.post || [],
        rejection.attachments || []
      )

      snackbar.error(errors[0])
    } else {
      snackbar.apiError(rejection)
    }
  }

  close = () => {
    this.minimize()
    posting.close()
  }

  minimize = () => {
    this.setState({ fullscreen: false, minimized: true })
  }

  open = () => {
    this.setState({ minimized: false })
    if (this.state.fullscreen) {
    }
  }

  fullscreenEnter = () => {
    this.setState({ fullscreen: true, minimized: false })
  }

  fullscreenExit = () => {
    this.setState({ fullscreen: false, minimized: false })
  }

  render() {
    const dialogProps = {
      minimized: this.state.minimized,
      minimize: this.minimize,
      open: this.open,

      fullscreen: this.state.fullscreen,
      fullscreenEnter: this.fullscreenEnter,
      fullscreenExit: this.fullscreenExit,

      close: this.onCancel,
    }

    return (
      <PostingDialogStartPrivate {...dialogProps}>
        <form className="posting-dialog-form" onSubmit={this.handleSubmit}>
          <Toolbar className="posting-dialog-toolbar">
            <ToolbarSection className="posting-dialog-thread-recipients" auto>
              <ToolbarItem auto>
                <input
                  className="form-control"
                  disabled={this.state.isLoading}
                  onChange={this.onToChange}
                  placeholder={pgettext(
                    "post thread",
                    "Recipients, eg.: Danny, Lisa, Alice"
                  )}
                  type="text"
                  value={this.state.to}
                />
              </ToolbarItem>
            </ToolbarSection>
            <ToolbarSection className="posting-dialog-thread-title" auto>
              <ToolbarItem auto>
                <input
                  className="form-control"
                  disabled={this.state.isLoading}
                  onChange={this.onTitleChange}
                  placeholder={pgettext("post thread", "Thread title")}
                  type="text"
                  value={this.state.title}
                />
              </ToolbarItem>
            </ToolbarSection>
          </Toolbar>
          <MarkupEditor
            attachments={this.state.attachments}
            value={this.state.post}
            submitText={pgettext("post thread submit", "Start thread")}
            disabled={this.state.isLoading}
            onAttachmentsChange={this.onAttachmentsChange}
            onChange={this.onPostChange}
          />
        </form>
      </PostingDialogStartPrivate>
    )
  }
}

const PostingDialogStartPrivate = ({
  children,
  close,
  minimized,
  minimize,
  open,
  fullscreen,
  fullscreenEnter,
  fullscreenExit,
}) => (
  <PostingDialog fullscreen={fullscreen} minimized={minimized}>
    <PostingDialogHeader
      fullscreen={fullscreen}
      fullscreenEnter={fullscreenEnter}
      fullscreenExit={fullscreenExit}
      minimized={minimized}
      minimize={minimize}
      open={open}
      close={close}
    >
      {pgettext("post thread", "Start private thread")}
    </PostingDialogHeader>
    <PostingDialogBody>{children}</PostingDialogBody>
  </PostingDialog>
)
