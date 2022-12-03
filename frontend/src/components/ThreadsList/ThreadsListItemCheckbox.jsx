import React from "react"
import * as select from "misago/reducers/selection"
import store from "misago/services/store"

const ThreadsListItemCheckbox = ({ checked, disabled, thread }) => (
  <button
    className="btn btn-default btn-icon"
    type="button"
    disabled={disabled}
    onClick={() => store.dispatch(select.item(thread.id))}
  >
    <span className="material-icon">
      {checked ? "check_box" : "check_box_outline_blank"}
    </span>
  </button>
)

export default ThreadsListItemCheckbox
