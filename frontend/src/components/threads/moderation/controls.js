import React from "react"
import ErrorsModal from "misago/components/threads/moderation/errors-list"
import MergeThreads from "misago/components/threads/moderation/merge"
import MoveThreads from "misago/components/threads/moderation/move"
import * as select from "misago/reducers/selection"
import ajax from "misago/services/ajax"
import modal from "misago/services/modal"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends React.Component {
  callApi = (ops, successMessage, onSuccess = null) => {
    // freeze threads
    this.props.threads.forEach((thread) => {
      this.props.freezeThread(thread.id)
    })

    // list ids
    const ids = this.props.threads.map((thread) => {
      return thread.id
    })

    // always return current acl
    ops.push({ op: "add", path: "acl", value: true })

    ajax.patch(this.props.api, { ids, ops }).then(
      (data) => {
        // unfreeze
        this.props.threads.forEach((thread) => {
          this.props.freezeThread(thread.id)
        })

        // update threads
        data.forEach((thread) => {
          this.props.updateThread(thread)
        })

        // show success message and call callback
        snackbar.success(successMessage)
        if (onSuccess) {
          onSuccess()
        }
      },
      (rejection) => {
        // unfreeze
        this.props.threads.forEach((thread) => {
          this.props.freezeThread(thread.id)
        })

        // escape on non-400 error
        if (rejection.status !== 400) {
          return snackbar.apiError(rejection)
        }

        // build errors list
        let errors = []
        let threadsMap = {}

        this.props.threads.forEach((thread) => {
          threadsMap[thread.id] = thread
        })

        rejection.forEach(({ id, detail }) => {
          if (typeof threadsMap[id] !== "undefined") {
            errors.push({
              errors: detail,
              thread: threadsMap[id],
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
          value: 2,
        },
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
          value: 1,
        },
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
          value: 0,
        },
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
          value: false,
        },
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
          value: false,
        },
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
          value: true,
        },
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
          value: false,
        },
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
          value: true,
        },
      ],
      gettext("Selected threads were hidden.")
    )
  }

  move = () => {
    modal.show(
      <MoveThreads
        callApi={this.callApi}
        category={this.props.category}
        categories={this.props.categories}
        categoriesMap={this.props.categoriesMap}
        user={this.props.user}
      />
    )
  }

  merge = () => {
    const errors = []
    this.props.threads.forEach((thread) => {
      if (!thread.acl.can_merge) {
        errors.append({
          id: thread.id,
          title: thread.title,
          errors: [
            gettext(
              "You don't have permission to merge this thread with others."
            ),
          ],
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
      !window.confirm(
        gettext("Are you sure you want to delete selected threads?")
      )
    ) {
      return
    }

    this.props.threads.map((thread) => {
      this.props.freezeThread(thread.id)
    })

    const ids = this.props.threads.map((thread) => {
      return thread.id
    })

    ajax.delete(this.props.api, ids).then(
      () => {
        this.props.threads.map((thread) => {
          this.props.freezeThread(thread.id)
          this.props.deleteThread(thread)
        })

        snackbar.success(gettext("Selected threads were deleted."))
      },
      (rejection) => {
        if (rejection.status === 400) {
          const failedThreads = rejection.map((thread) => {
            return thread.id
          })

          this.props.threads.map((thread) => {
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

  render() {
    const { moderation, threads } = this.props
    const noSelection = this.props.selection.length == 0

    return (
      <ul className="dropdown-menu dropdown-menu-right stick-to-bottom">
        <li>
          <button
            className="btn btn-link"
            type="button"
            onClick={() => store.dispatch(select.all(threads.map((t) => t.id)))}
          >
            <span className="material-icon">check_box</span>
            {gettext("Select all")}
          </button>
        </li>
        <li>
          <button
            className="btn btn-link"
            type="button"
            disabled={noSelection}
            onClick={() => store.dispatch(select.none())}
          >
            <span className="material-icon">check_box_outline_blank</span>
            {gettext("Select none")}
          </button>
        </li>
        <li role="separator" className="divider" />
        {!!moderation.can_pin_globally && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.pinGlobally}
            >
              <span className="material-icon">bookmark</span>
              {gettext("Pin threads globally")}
            </button>
          </li>
        )}
        {!!moderation.can_pin && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.pinLocally}
            >
              <span className="material-icon">bookmark_border</span>
              {gettext("Pin threads locally")}
            </button>
          </li>
        )}
        {!!moderation.can_pin && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.unpin}
            >
              <span className="material-icon">panorama_fish_eye</span>
              {gettext("Unpin threads")}
            </button>
          </li>
        )}
        {!!moderation.can_move && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.move}
            >
              <span className="material-icon">arrow_forward</span>
              {gettext("Move threads")}
            </button>
          </li>
        )}
        {!!moderation.can_merge && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.merge}
            >
              <span className="material-icon">call_merge</span>
              {gettext("Merge threads")}
            </button>
          </li>
        )}
        {!!moderation.can_approve && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.approve}
            >
              <span className="material-icon">done</span>
              {gettext("Approve threads")}
            </button>
          </li>
        )}
        {!!moderation.can_close && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.open}
            >
              <span className="material-icon">lock_open</span>
              {gettext("Open threads")}
            </button>
          </li>
        )}
        {!!moderation.can_close && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.close}
            >
              <span className="material-icon">lock_outline</span>
              {gettext("Close threads")}
            </button>
          </li>
        )}
        {!!moderation.can_unhide && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.unhide}
            >
              <span className="material-icon">visibility</span>
              {gettext("Unhide threads")}
            </button>
          </li>
        )}
        {!!moderation.can_hide && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.hide}
            >
              <span className="material-icon">visibility_off</span>
              {gettext("Hide threads")}
            </button>
          </li>
        )}
        {!!moderation.can_delete && (
          <li>
            <button
              className="btn btn-link"
              type="button"
              disabled={noSelection}
              onClick={this.delete}
            >
              <span className="material-icon">clear</span>
              {gettext("Delete threads")}
            </button>
          </li>
        )}
      </ul>
    )
  }
}
