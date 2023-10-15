import React from "react"
import CategorySelect from "misago/components/category-select"
import Form from "misago/components/form"
import * as attachments from "./utils/attachments"
import { getPostValidators, getTitleValidators } from "./utils/validators"
import ajax from "misago/services/ajax"
import posting from "misago/services/posting"
import snackbar from "misago/services/snackbar"
import MarkupEditor from "../MarkupEditor"
import { Toolbar, ToolbarItem, ToolbarSection } from "../Toolbar"
import PostingDialog from "./PostingDialog"
import PostingDialogBody from "./PostingDialogBody"
import PostingDialogError from "./PostingDialogError"
import PostingDialogHeader from "./PostingDialogHeader"
import PostingThreadOptions from "./PostingThreadOptions"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isReady: false,
      isLoading: false,

      error: null,

      minimized: false,
      fullscreen: false,

      options: null,

      title: "",
      category: props.category || null,
      categories: [],
      post: "",
      attachments: [],
      close: false,
      hide: false,
      pin: 0,

      validators: {
        title: getTitleValidators(),
        post: getPostValidators(),
      },
      errors: {},
    }
  }

  componentDidMount() {
    ajax.get(this.props.config).then(this.loadSuccess, this.loadError)
  }

  loadSuccess = (data) => {
    let category = null
    let options = null

    // hydrate categories, extract posting options
    const categories = data.map((item) => {
      // pick first category that allows posting and if it may, override it with initial one
      if (
        item.post !== false &&
        (!category || item.id == this.state.category)
      ) {
        category = item.id
        options = item.post
      }

      return Object.assign(item, {
        disabled: item.post === false,
        label: item.name,
        value: item.id,
      })
    })

    this.setState({
      isReady: true,
      options,

      categories,
      category,
    })
  }

  loadError = (rejection) => {
    this.setState({
      error: rejection.detail,
    })
  }

  onCancel = () => {
    const formEmpty = !!(
      this.state.post.length === 0 &&
      this.state.title.length === 0 &&
      this.state.attachments.length === 0
    )

    if (formEmpty) {
      this.minimize()
      return posting.close()
    }

    const cancel = window.confirm(
      pgettext("post thread", "Are you sure you want to discard thread?")
    )
    if (cancel) {
      this.minimize()
      posting.close()
    }
  }

  onTitleChange = (event) => {
    this.changeValue("title", event.target.value)
  }

  onCategoryChange = (event) => {
    const category = this.state.categories.find((item) => {
      return event.target.value == item.value
    })

    // if selected pin is greater than allowed, reduce it
    let pin = this.state.pin
    if (category.post.pin && category.post.pin < pin) {
      pin = category.post.pin
    }

    this.setState({
      category: category.id,
      categoryOptions: category.post,

      pin,
    })
  }

  onPostChange = (event) => {
    this.changeValue("post", event.target.value)
  }

  onAttachmentsChange = (attachments) => {
    this.setState(attachments)
  }

  onClose = () => {
    this.changeValue("close", true)
  }

  onOpen = () => {
    this.changeValue("close", false)
  }

  onPinGlobally = () => {
    this.changeValue("pin", 2)
  }

  onPinLocally = () => {
    this.changeValue("pin", 1)
  }

  onUnpin = () => {
    this.changeValue("pin", 0)
  }

  onHide = () => {
    this.changeValue("hide", true)
  }

  onUnhide = () => {
    this.changeValue("hide", false)
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

  clean() {
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
      title: this.state.title,
      category: this.state.category,
      post: this.state.post,
      attachments: attachments.clean(this.state.attachments),
      close: this.state.close,
      hide: this.state.hide,
      pin: this.state.pin,
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
    const dialogProps = {
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
        <PostingDialogStart {...dialogProps}>
          <PostingDialogError message={this.state.error} close={this.close} />
        </PostingDialogStart>
      )
    }

    if (!this.state.isReady) {
      return (
        <PostingDialogStart {...dialogProps}>
          <div className="posting-loading ui-preview">
            <Toolbar className="posting-dialog-toolbar">
              <ToolbarSection className="posting-dialog-thread-title" auto>
                <ToolbarItem auto>
                  <input className="form-control" disabled={true} type="text" />
                </ToolbarItem>
              </ToolbarSection>
              <ToolbarSection className="posting-dialog-category-select" auto>
                <ToolbarItem>
                  <input className="form-control" disabled={true} type="text" />
                </ToolbarItem>
              </ToolbarSection>
            </Toolbar>
            <MarkupEditor
              attachments={[]}
              value={""}
              submitText={pgettext("post thread submit", "Start thread")}
              disabled={true}
              onAttachmentsChange={() => {}}
              onChange={() => {}}
            />
          </div>
        </PostingDialogStart>
      )
    }

    const showOptions = !!(
      this.state.options.close ||
      this.state.options.hide ||
      this.state.options.pin
    )

    return (
      <PostingDialogStart {...dialogProps}>
        <form className="posting-dialog-form" onSubmit={this.handleSubmit}>
          <Toolbar className="posting-dialog-toolbar">
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
            <ToolbarSection className="posting-dialog-category-select" auto>
              <ToolbarItem>
                <CategorySelect
                  choices={this.state.categories}
                  disabled={this.state.isLoading}
                  onChange={this.onCategoryChange}
                  value={this.state.category}
                />
              </ToolbarItem>
              {showOptions && (
                <ToolbarItem shrink>
                  <PostingThreadOptions
                    isClosed={this.state.close}
                    isHidden={this.state.hide}
                    isPinned={this.state.pin}
                    disabled={this.state.isLoading}
                    options={this.state.options}
                    close={this.onClose}
                    open={this.onOpen}
                    hide={this.onHide}
                    unhide={this.onUnhide}
                    pinGlobally={this.onPinGlobally}
                    pinLocally={this.onPinLocally}
                    unpin={this.onUnpin}
                  />
                </ToolbarItem>
              )}
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
      </PostingDialogStart>
    )
  }
}

const PostingDialogStart = ({
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
      {pgettext("post thread", "Start new thread")}
    </PostingDialogHeader>
    <PostingDialogBody>{children}</PostingDialogBody>
  </PostingDialog>
)
