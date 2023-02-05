import React from "react"
import Form from "misago/components/form"
import * as attachments from "./utils/attachments"
import { getPostValidators } from "./utils/validators"
import ajax from "misago/services/ajax"
import posting from "misago/services/posting"
import snackbar from "misago/services/snackbar"
import MarkupEditor from "../MarkupEditor"
import PostingDialog from "./PostingDialog"
import PostingDialogBody from "./PostingDialogBody"
import PostingDialogError from "./PostingDialogError"
import PostingDialogHeader from "./PostingDialogHeader"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isReady: false,
      isLoading: false,

      error: null,

      minimized: false,
      fullscreen: false,

      post: "",
      attachments: [],

      validators: {
        post: getPostValidators(),
      },
      errors: {},
    }
  }

  componentDidMount() {
    ajax
      .get(this.props.config, this.props.context || null)
      .then(this.loadSuccess, this.loadError)
  }

  componentWillReceiveProps(nextProps) {
    const context = this.props.context
    const newContext = nextProps.context

    if (context && newContext && context.reply === newContext.reply) return

    ajax
      .get(nextProps.config, nextProps.context || null)
      .then(this.appendData, snackbar.apiError)
  }

  loadSuccess = (data) => {
    this.setState({
      isReady: true,

      post: data.post
        ? '[quote="@' + data.poster + '"]\n' + data.post + "\n[/quote]"
        : "",
    })
  }

  loadError = (rejection) => {
    this.setState({
      error: rejection.detail,
    })
  }

  appendData = (data) => {
    const newPost = data.post
      ? '[quote="@' + data.poster + '"]\n' + data.post + "\n[/quote]\n\n"
      : ""

    this.setState((prevState, props) => {
      if (prevState.post.length > 0) {
        return {
          post: prevState.post + "\n\n" + newPost,
        }
      }

      return {
        post: newPost,
      }
    })
  }

  onCancel = () => {
    const cancel = window.confirm(
      gettext("Are you sure you want to discard your reply?")
    )
    if (cancel) {
      this.close()
    }
  }

  onPostChange = (event) => {
    this.changeValue("post", event.target.value)
  }

  onAttachmentsChange = (attachments) => {
    this.setState(attachments)
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
    return ajax.post(this.props.submit, {
      post: this.state.post,
      attachments: attachments.clean(this.state.attachments),
    })
  }

  handleSuccess(success) {
    snackbar.success(gettext("Your reply has been posted."))
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
      thread: this.props.thread,

      minimized: this.state.minimized,
      minimize: this.minimize,
      open: this.open,

      fullscreen: this.state.fullscreen,
      fullscreenEnter: this.fullscreenEnter,
      fullscreenExit: this.fullscreenExit,

      close: this.onCancel,
    }

    if (this.state.error) {
      return (
        <PostingDialogReply {...dialogProps}>
          <PostingDialogError message={this.state.error} close={this.close} />
        </PostingDialogReply>
      )
    }

    if (!this.state.isReady) {
      return (
        <PostingDialogReply {...dialogProps}>
          <div className="posting-loading ui-preview">
            <MarkupEditor
              attachments={[]}
              value={""}
              submitText={pgettext("post reply", "Post reply")}
              disabled={true}
              onAttachmentsChange={() => {}}
              onChange={() => {}}
            />
          </div>
        </PostingDialogReply>
      )
    }

    return (
      <PostingDialogReply {...dialogProps}>
        <form
          className="posting-dialog-form"
          method="POST"
          onSubmit={this.handleSubmit}
        >
          <MarkupEditor
            attachments={this.state.attachments}
            value={this.state.post}
            submitText={pgettext("post reply", "Post reply")}
            disabled={this.state.isLoading}
            onAttachmentsChange={this.onAttachmentsChange}
            onChange={this.onPostChange}
          />
        </form>
      </PostingDialogReply>
    )
  }
}

const PostingDialogReply = ({
  children,
  close,
  minimized,
  minimize,
  open,
  fullscreen,
  fullscreenEnter,
  fullscreenExit,
  thread,
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
      {interpolate(
        pgettext("post reply", "Reply to: %(thread)s"),
        { thread: thread.title },
        true
      )}
    </PostingDialogHeader>
    <PostingDialogBody>{children}</PostingDialogBody>
  </PostingDialog>
)
