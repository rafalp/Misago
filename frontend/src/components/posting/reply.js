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
import { clearGlobalState, setGlobalState } from "./globalState"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isReady: false,
      isLoading: false,

      error: null,

      minimized: false,
      fullscreen: false,

      post: this.props.default || "",
      attachments: [],

      validators: {
        post: getPostValidators(),
      },
      errors: {},
    }

    this.quoteText = ""
  }

  componentDidMount() {
    ajax
      .get(this.props.config, this.props.context || null)
      .then(this.loadSuccess, this.loadError)

    setGlobalState(false, this.onQuote)
  }

  componentWillUnmount() {
    clearGlobalState()
  }

  componentWillReceiveProps(nextProps) {
    const context = this.props.context
    const newContext = nextProps.context

    // User clicked "reply" instead of "quote"
    if (context && newContext && !newContext.reply) return

    ajax
      .get(nextProps.config, nextProps.context || null)
      .then(this.appendData, snackbar.apiError)
  }

  loadSuccess = (data) => {
    this.setState({
      isReady: true,

      post: data.post
        ? '[quote="@' + data.poster + '"]\n' + data.post + "\n[/quote]"
        : this.state.post,
    })

    this.quoteText = data.post
      ? '[quote="@' + data.poster + '"]\n' + data.post + "\n[/quote]"
      : this.state.post
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
          post: prevState.post.trim() + "\n\n" + newPost,
        }
      }

      return {
        post: newPost,
      }
    })

    this.open()
  }

  onCancel = () => {
    // If only the quote text is on editor user didn't add anything
    // so no changes to discard
    const onlyQuoteTextInEditor = this.state.post === this.quoteText

    if (onlyQuoteTextInEditor && this.state.attachments.length === 0) {
      return this.close()
    }

    const cancel = window.confirm(
      pgettext("post reply", "Are you sure you want to discard your reply?")
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

  onQuote = (quote) => {
    this.setState(({ post }) => {
      if (post.length > 0) {
        return { post: post.trim() + "\n\n" + quote }
      }

      return { post: quote }
    })

    this.open()
  }

  clean() {
    if (!this.state.post.trim().length) {
      snackbar.error(pgettext("posting form", "You have to enter a message."))
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
    setGlobalState(true, this.onQuote)

    return ajax.post(this.props.submit, {
      post: this.state.post,
      attachments: attachments.clean(this.state.attachments),
    })
  }

  handleSuccess(success) {
    this.setState({ isLoading: true })
    this.close()

    setGlobalState(false, this.onQuote)

    snackbar.success(pgettext("post reply", "Your reply has been posted."))
    window.location = success.url.index
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

    setGlobalState(false, this.onQuote)
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
              submitText={pgettext("post reply submit", "Post reply")}
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
            submitText={pgettext("post reply submit", "Post reply")}
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
