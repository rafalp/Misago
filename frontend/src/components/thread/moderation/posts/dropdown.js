import React from "react"
import modal from "misago/services/modal"
import * as moderation from "./actions"
import MoveModal from "./move"
import SplitModal from "./split"

export default function (props) {
  return (
    <ul className="dropdown-menu dropdown-menu-right stick-to-bottom">
      <Approve {...props} />
      <Merge {...props} />
      <Move {...props} />
      <Split {...props} />
      <Protect {...props} />
      <Unprotect {...props} />
      <Unhide {...props} />
      <Hide {...props} />
      <Delete {...props} />
    </ul>
  )
}

export class Approve extends React.Component {
  onClick = () => {
    moderation.approve(this.props)
  }

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_approve && post.is_unapproved
    })

    if (!isVisible) return null

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">done</span>
          {pgettext("thread posts moderation", "Approve")}
        </button>
      </li>
    )
  }
}

export class Merge extends React.Component {
  onClick = () => {
    moderation.merge(this.props)
  }

  render() {
    const isVisible =
      this.props.selection.length > 1 &&
      this.props.selection.find((post) => {
        return post.acl.can_merge
      })

    if (!isVisible) return null

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">call_merge</span>
          {pgettext("thread posts moderation", "Merge")}
        </button>
      </li>
    )
  }
}

export class Move extends React.Component {
  onClick = () => {
    modal.show(<MoveModal {...this.props} />)
  }

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_move
    })

    if (!isVisible) return null

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">arrow_forward</span>
          {pgettext("thread posts moderation", "Move")}
        </button>
      </li>
    )
  }
}

export class Split extends React.Component {
  onClick = () => {
    modal.show(<SplitModal {...this.props} />)
  }

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_move
    })

    if (!isVisible) return null

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">call_split</span>
          {pgettext("thread posts moderation", "Split")}
        </button>
      </li>
    )
  }
}

export class Protect extends React.Component {
  onClick = () => {
    moderation.protect(this.props)
  }

  render() {
    const isVisible = this.props.selection.find((post) => {
      return !post.is_protected && post.acl.can_protect
    })

    if (!isVisible) return null

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">lock_outline</span>
          {pgettext("thread posts moderation", "Protect")}
        </button>
      </li>
    )
  }
}

export class Unprotect extends React.Component {
  onClick = () => {
    moderation.unprotect(this.props)
  }

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.is_protected && post.acl.can_protect
    })

    if (!isVisible) return null

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">lock_open</span>
          {pgettext("thread posts moderation", "Unprotect")}
        </button>
      </li>
    )
  }
}

export class Hide extends React.Component {
  onClick = () => {
    moderation.hide(this.props)
  }

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_hide && !post.is_hidden
    })

    if (!isVisible) return null

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">visibility_off</span>
          {pgettext("thread posts moderation", "Hide")}
        </button>
      </li>
    )
  }
}

export class Unhide extends React.Component {
  onClick = () => {
    moderation.unhide(this.props)
  }

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_unhide && post.is_hidden
    })

    if (!isVisible) return null

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">visibility</span>
          {pgettext("thread posts moderation", "Unhide")}
        </button>
      </li>
    )
  }
}

export class Delete extends React.Component {
  onClick = () => {
    moderation.remove(this.props)
  }

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_delete
    })

    if (!isVisible) return null

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">clear</span>
          {pgettext("thread posts moderation", "Delete")}
        </button>
      </li>
    )
  }
}
