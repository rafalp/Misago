import React from "react"

const ThreadsListUpdatePrompt = ({ threads, onClick }) => (
  <li className="list-group-item threads-list-update-prompt">
    <button
      type="button"
      className="btn btn-block threads-list-update-prompt-btn"
      onClick={onClick}
    >
      <span className="material-icon">cached</span>
      <span className="threads-list-update-prompt-message">
        {interpolate(
          ngettext(
            "There is %(threads)s new or updated thread. Click here to show it.",
            "There are %(threads)s new or updated threads. Click here to show them.",
            threads
          ),
          { threads },
          true
        )}
      </span>
    </button>
  </li>
)

export default ThreadsListUpdatePrompt
