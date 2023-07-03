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

      error: false,

      minimized: false,
      fullscreen: false,

      post: "",
      attachments: [],
      protect: false,

      canProtect: false,

      validators: {
        post: getPostValidators(),
      },
      errors: {},
    }

    this.originalPost = ""
  }

  componentDidMount() {
    ajax.get(this.props.config).then(this.loadSuccess, this.loadError)

    setGlobalState(false, this.onQuote)
  }

  componentWillUnmount() {
    clearGlobalState()
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
    this.originalPost = data.post

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
    const originalPostSameAsCurrentPost =
      this.state.originalPost === this.state.post
    const noAttachementsAdded = this.state.attachments.length === 0

    if (originalPostSameAsCurrentPost && noAttachementsAdded) {
      return this.close()
    }

    const cancel = window.confirm(
      pgettext("edit reply", "Are you sure you want to discard changes?")
    )
    if (cancel) {
      this.close()
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

    return ajax.put(this.props.submit, {
      post: this.state.post,
      attachments: attachments.clean(this.state.attachments),
      protect: this.state.protect,
    })
  }

  handleSuccess(success) {
    this.setState({ isLoading: true })
    this.close()

    setGlobalState(false, this.onQuote)

    snackbar.success(pgettext("edit reply", "Reply has been edited."))
    window.location = success.url.index
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
      post: this.props.post,

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
        <PostingDialogEditReply {...dialogProps}>
          <PostingDialogError message={this.state.error} close={this.close} />
        </PostingDialogEditReply>
      )
    }

    if (!this.state.isReady) {
      return (
        <PostingDialogEditReply {...dialogProps}>
          <div className="posting-loading ui-preview">
            <MarkupEditor
              attachments={[]}
              value={""}
              submitText={pgettext("edit reply submit", "Edit reply")}
              disabled={true}
              onAttachmentsChange={() => {}}
              onChange={() => {}}
            />
          </div>
        </PostingDialogEditReply>
      )
    }

    return (
      <PostingDialogEditReply {...dialogProps}>
        <form
          className="posting-dialog-form"
          method="POST"
          onSubmit={this.handleSubmit}
        >
          <MarkupEditor
            attachments={this.state.attachments}
            canProtect={this.state.canProtect}
            isProtected={this.state.protect}
            enableProtection={() => this.setState({ protect: true })}
            disableProtection={() => this.setState({ protect: false })}
            value={this.state.post}
            submitText={pgettext("edit reply submit", "Edit reply")}
            disabled={this.state.isLoading}
            onAttachmentsChange={this.onAttachmentsChange}
            onChange={this.onPostChange}
          />
        </form>
      </PostingDialogEditReply>
    )
  }
}

const PostingDialogEditReply = ({
  children,
  close,
  minimized,
  minimize,
  open,
  fullscreen,
  fullscreenEnter,
  fullscreenExit,
  post,
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
        pgettext("edit reply", "Edit reply by %(poster)s from %(date)s"),
        {
          poster: post.poster ? post.poster.username : post.poster_name,
          date: post.posted_on.fromNow(),
        },
        true
      )}
    </PostingDialogHeader>
    <PostingDialogBody>{children}</PostingDialogBody>
  </PostingDialog>
)
