import React from "react"
import Button from "misago/components/button"
import escapeHtml from "misago/utils/escape-html"

const DATE_ABBR = '<abbr title="%(absolute)s">%(relative)s</abbr>'
const USER_SPAN = '<span class="item-title">%(user)s</span>'
const USER_URL = '<a href="%(url)s" class="item-title">%(user)s</a>'

export default class extends React.Component {
  goLast = () => {
    this.props.goToEdit()
  }

  goForward = () => {
    this.props.goToEdit(this.props.edit.next)
  }

  goBack = () => {
    this.props.goToEdit(this.props.edit.previous)
  }

  revertEdit = () => {
    this.props.revertEdit(this.props.edit.id)
  }

  render() {
    return (
      <div className="modal-toolbar post-changelog-toolbar">
        <div className="row">
          <div className="col-xs-12 col-sm-4">
            <div className="row">
              <div className="col-xs-4">
                <GoBackBtn
                  disabled={this.props.disabled}
                  edit={this.props.edit}
                  onClick={this.goBack}
                />
              </div>
              <div className="col-xs-4">
                <GoForwardBtn
                  disabled={this.props.disabled}
                  edit={this.props.edit}
                  onClick={this.goForward}
                />
              </div>
              <div className="col-xs-4">
                <GoLastBtn
                  disabled={this.props.disabled}
                  edit={this.props.edit}
                  onClick={this.goLast}
                />
              </div>
            </div>
          </div>
          <div className="col-xs-12 col-sm-5 xs-margin-top-half post-change-label">
            <Label edit={this.props.edit} />
          </div>
          <RevertBtn
            canRevert={this.props.canRevert}
            disabled={this.props.disabled}
            onClick={this.revertEdit}
          />
        </div>
      </div>
    )
  }
}

export function GoBackBtn(props) {
  return (
    <Button
      className="btn-default btn-block btn-icon btn-sm"
      disabled={props.disabled || !props.edit.previous}
      onClick={props.onClick}
      title={pgettext("post history modal btn", "See previous change")}
    >
      <span className="material-icon">chevron_left</span>
    </Button>
  )
}

export function GoForwardBtn(props) {
  return (
    <Button
      className="btn-default btn-block btn-icon btn-sm"
      disabled={props.disabled || !props.edit.next}
      onClick={props.onClick}
      title={pgettext("post history modal btn", "See next change")}
    >
      <span className="material-icon">chevron_right</span>
    </Button>
  )
}

export function GoLastBtn(props) {
  return (
    <Button
      className="btn-default btn-block btn-icon btn-sm"
      disabled={props.disabled || !props.edit.next}
      onClick={props.onClick}
      title={pgettext("post history modal btn", "See previous change")}
    >
      <span className="material-icon">last_page</span>
    </Button>
  )
}

export function RevertBtn(props) {
  if (!props.canRevert) return null

  return (
    <div className="col-sm-3 hidden-xs">
      <Button
        className="btn-default btn-sm btn-block"
        disabled={props.disabled}
        onClick={props.onClick}
        title={pgettext(
          "post revert btn",
          "Revert post to state from before this edit."
        )}
      >
        {pgettext("post revert btn", "Revert")}
      </Button>
    </div>
  )
}

export function Label(props) {
  let user = null
  if (props.edit.url.editor) {
    user = interpolate(
      USER_URL,
      {
        url: escapeHtml(props.edit.url.editor),
        user: escapeHtml(props.edit.editor_name),
      },
      true
    )
  } else {
    user = interpolate(
      USER_SPAN,
      {
        user: escapeHtml(props.edit.editor_name),
      },
      true
    )
  }

  const date = interpolate(
    DATE_ABBR,
    {
      absolute: escapeHtml(props.edit.edited_on.format("LLL")),
      relative: escapeHtml(props.edit.edited_on.fromNow()),
    },
    true
  )

  const message = interpolate(
    escapeHtml(
      pgettext("post history modal", "By %(edited_by)s %(edited_on)s.")
    ),
    {
      edited_by: user,
      edited_on: date,
    },
    true
  )

  return <p dangerouslySetInnerHTML={{ __html: message }} />
}
