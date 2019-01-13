import React from "react"
import ErrorsModal from "misago/components/threads/moderation/errors-list"
import MergeThreads from "misago/components/threads/moderation/merge"
import MoveThreads from "misago/components/threads/moderation/move"
import * as select from "misago/reducers/selection"
import ajax from "misago/services/ajax"
import modal from "misago/services/modal"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"
import Countdown from "misago/utils/countdown"

export default class extends React.Component {
  callApi = (ops, successMessage, onSuccess = null) => {
    // freeze threads
    this.props.threads.forEach(thread => {
      this.props.freezeThread(thread.id)
    })

    // list ids
    const ids = this.props.threads.map(thread => {
      return thread.id
    })

    // always return current acl
    ops.push({ op: "add", path: "acl", value: true })

    ajax.patch(this.props.api, { ids, ops }).then(
      data => {
        // unfreeze
        this.props.threads.forEach(thread => {
          this.props.freezeThread(thread.id)
        })

        // update threads
        data.forEach(thread => {
          this.props.updateThread(thread)
        })

        // show success message and call callback
        snackbar.success(successMessage)
        if (onSuccess) {
          onSuccess()
        }
      },
      rejection => {
        // unfreeze
        this.props.threads.forEach(thread => {
          this.props.freezeThread(thread.id)
        })

        // escape on non-400 error
        if (rejection.status !== 400) {
          return snackbar.apiError(rejection)
        }

        // build errors list
        let errors = []
        let threadsMap = {}

        this.props.threads.forEach(thread => {
          threadsMap[thread.id] = thread
        })

        rejection.forEach(({ id, detail }) => {
          if (typeof threadsMap[id] !== "undefined") {
            errors.push({
              errors: detail,
              thread: threadsMap[id]
            })
          }
        })

        modal.show(<ErrorsModal errors={errors} />)
      }
    )
  }

  pinGlobally = () => {
    this.callApi(
      [
        {
          op: "replace",
          path: "weight",
          value: 2
        }
      ],
      gettext("Selected threads were pinned globally.")
    )
  }

  pinLocally = () => {
    this.callApi(
      [
        {
          op: "replace",
          path: "weight",
          value: 1
        }
      ],
      gettext("Selected threads were pinned locally.")
    )
  }

  unpin = () => {
    this.callApi(
      [
        {
          op: "replace",
          path: "weight",
          value: 0
        }
      ],
      gettext("Selected threads were unpinned.")
    )
  }

  approve = () => {
    this.callApi(
      [
        {
          op: "replace",
          path: "is-unapproved",
          value: false
        }
      ],
      gettext("Selected threads were approved.")
    )
  }

  open = () => {
    this.callApi(
      [
        {
          op: "replace",
          path: "is-closed",
          value: false
        }
      ],
      gettext("Selected threads were opened.")
    )
  }

  close = () => {
    this.callApi(
      [
        {
          op: "replace",
          path: "is-closed",
          value: true
        }
      ],
      gettext("Selected threads were closed.")
    )
  }

  unhide = () => {
    this.callApi(
      [
        {
          op: "replace",
          path: "is-hidden",
          value: false
        }
      ],
      gettext("Selected threads were unhidden.")
    )
  }

  hide = () => {
    this.callApi(
      [
        {
          op: "replace",
          path: "is-hidden",
          value: true
        }
      ],
      gettext("Selected threads were hidden.")
    )
  }

  move = () => {
    modal.show(
      <MoveThreads
        callApi={this.callApi}
        categories={this.props.categories}
        categoriesMap={this.props.categoriesMap}
        route={this.props.route}
        user={this.props.user}
      />
    )
  }

  merge = () => {
    const errors = []
    this.props.threads.forEach(thread => {
      if (!thread.acl.can_merge) {
        errors.append({
          id: thread.id,
          title: thread.title,
          errors: [
            gettext(
              "You don't have permission to merge this thread with others."
            )
          ]
        })
      }
    })

    if (this.props.threads.length < 2) {
      snackbar.info(
        gettext("You have to select at least two threads to merge.")
      )
    } else if (errors.length) {
      modal.show(<ErrorsModal errors={errors} />)
      return
    } else {
      modal.show(<MergeThreads {...this.props} />)
    }
  }

  delete = () => {
    if (
      !confirm(gettext("Are you sure you want to delete selected threads?"))
    ) {
      return
    }

    this.props.threads.map(thread => {
      this.props.freezeThread(thread.id)
    })

    const ids = this.props.threads.map(thread => {
      return thread.id
    })

    ajax.delete(this.props.api, ids).then(
      () => {
        this.props.threads.map(thread => {
          this.props.freezeThread(thread.id)
          this.props.deleteThread(thread)
        })

        snackbar.success(gettext("Selected threads were deleted."))
      },
      rejection => {
        if (rejection.status === 400) {
          const failedThreads = rejection.map(thread => {
            return thread.id
          })

          this.props.threads.map(thread => {
            this.props.freezeThread(thread.id)
            if (failedThreads.indexOf(thread.id) === -1) {
              this.props.deleteThread(thread)
            }
          })

          modal.show(<ErrorsModal errors={rejection} />)
        } else {
          snackbar.apiError(rejection)
        }
      }
    )
  }

  getPinGloballyButton() {
    if (!this.props.moderation.can_pin_globally) return null

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.pinGlobally}
          type="button"
        >
          <span className="material-icon">bookmark</span>
          {gettext("Pin threads globally")}
        </button>
      </li>
    )
  }

  getPinLocallyButton() {
    if (!this.props.moderation.can_pin) return null

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.pinLocally}
          type="button"
        >
          <span className="material-icon">bookmark_border</span>
          {gettext("Pin threads locally")}
        </button>
      </li>
    )
  }

  getUnpinButton() {
    if (!this.props.moderation.can_pin) return null

    return (
      <li>
        <button className="btn btn-link" onClick={this.unpin} type="button">
          <span className="material-icon">panorama_fish_eye</span>
          {gettext("Unpin threads")}
        </button>
      </li>
    )
  }

  getMoveButton() {
    if (!this.props.moderation.can_move) return null

    return (
      <li>
        <button className="btn btn-link" onClick={this.move} type="button">
          <span className="material-icon">arrow_forward</span>
          {gettext("Move threads")}
        </button>
      </li>
    )
  }

  getMergeButton() {
    if (!this.props.moderation.can_merge) return null

    return (
      <li>
        <button className="btn btn-link" onClick={this.merge} type="button">
          <span className="material-icon">call_merge</span>
          {gettext("Merge threads")}
        </button>
      </li>
    )
  }

  getApproveButton() {
    if (!this.props.moderation.can_approve) return null

    return (
      <li>
        <button className="btn btn-link" onClick={this.approve} type="button">
          <span className="material-icon">done</span>
          {gettext("Approve threads")}
        </button>
      </li>
    )
  }

  getOpenButton() {
    if (!this.props.moderation.can_close) return null

    return (
      <li>
        <button className="btn btn-link" onClick={this.open} type="button">
          <span className="material-icon">lock_open</span>
          {gettext("Open threads")}
        </button>
      </li>
    )
  }

  getCloseButton() {
    if (!this.props.moderation.can_close) return null

    return (
      <li>
        <button className="btn btn-link" onClick={this.close} type="button">
          <span className="material-icon">lock_outline</span>
          {gettext("Close threads")}
        </button>
      </li>
    )
  }

  getUnhideButton() {
    if (!this.props.moderation.can_unhide) return null

    return (
      <li>
        <button className="btn btn-link" onClick={this.unhide} type="button">
          <span className="material-icon">visibility</span>
          {gettext("Unhide threads")}
        </button>
      </li>
    )
  }

  getHideButton() {
    if (!this.props.moderation.can_hide) return null

    return (
      <li>
        <button onClick={this.hide} type="button" className="btn btn-link">
          <span className="material-icon">visibility_off</span>
          {gettext("Hide threads")}
        </button>
      </li>
    )
  }

  getDeleteButton() {
    if (!this.props.moderation.can_delete) return null

    return (
      <li>
        <button className="btn btn-link" onClick={this.delete} type="button">
          <span className="material-icon">clear</span>
          {gettext("Delete threads")}
        </button>
      </li>
    )
  }

  render() {
    return (
      <ul className={this.props.className}>
        {this.getPinGloballyButton()}
        {this.getPinLocallyButton()}
        {this.getUnpinButton()}
        {this.getMoveButton()}
        {this.getMergeButton()}
        {this.getApproveButton()}
        {this.getOpenButton()}
        {this.getCloseButton()}
        {this.getUnhideButton()}
        {this.getHideButton()}
        {this.getDeleteButton()}
      </ul>
    )
  }
}
