import React from "react"

export default function PostingThreadOptions({
  isClosed,
  isHidden,
  isPinned,
  disabled,
  options,
  close,
  open,
  hide,
  unhide,
  pinGlobally,
  pinLocally,
  unpin,
}) {
  const icons = getIcons(isClosed, isHidden, isPinned)

  return (
    <div className="dropdown">
      <button
        className="btn btn-default btn-outline btn-icon"
        title={pgettext("post thread", "Options")}
        aria-expanded="true"
        aria-haspopup="true"
        data-toggle="dropdown"
        type="button"
        disabled={disabled}
      >
        {icons.length > 0 ? (
          <span className="btn-icons-family">
            {icons.map((icon) => (
              <span key={icon} className="material-icon">
                {icon}
              </span>
            ))}
          </span>
        ) : (
          <span className="material-icon">more_horiz</span>
        )}
      </button>
      <ul className="dropdown-menu dropdown-menu-right stick-to-bottom">
        {options.pin === 2 && isPinned !== 2 && (
          <li>
            <button
              className="btn btn-link"
              onClick={pinGlobally}
              type="button"
              disabled={disabled}
            >
              <span className="material-icon">bookmark</span>
              {pgettext("post thread", "Pinned globally")}
            </button>
          </li>
        )}
        {options.pin >= isPinned && isPinned !== 1 && (
          <li>
            <button
              className="btn btn-link"
              onClick={pinLocally}
              type="button"
              disabled={disabled}
            >
              <span className="material-icon">bookmark_outline</span>
              {pgettext("post thread", "Pinned in category")}
            </button>
          </li>
        )}
        {options.pin >= isPinned && isPinned !== 0 && (
          <li>
            <button
              className="btn btn-link"
              onClick={unpin}
              type="button"
              disabled={disabled}
            >
              <span className="material-icon">radio_button_unchecked</span>
              {pgettext("post thread", "Not pinned")}
            </button>
          </li>
        )}
        {options.close && !!isClosed && (
          <li>
            <button
              className="btn btn-link"
              onClick={open}
              type="button"
              disabled={disabled}
            >
              <span className="material-icon">lock_outline</span>
              {pgettext("post thread", "Open")}
            </button>
          </li>
        )}
        {options.close && !isClosed && (
          <li>
            <button
              className="btn btn-link"
              onClick={close}
              type="button"
              disabled={disabled}
            >
              <span className="material-icon">lock</span>
              {pgettext("post thread", "Closed")}
            </button>
          </li>
        )}
        {options.hide && !!isHidden && (
          <li>
            <button
              className="btn btn-link"
              onClick={unhide}
              type="button"
              disabled={disabled}
            >
              <span className="material-icon">visibility</span>
              {pgettext("post thread", "Visible")}
            </button>
          </li>
        )}
        {options.hide && !isHidden && (
          <li>
            <button
              className="btn btn-link"
              onClick={hide}
              type="button"
              disabled={disabled}
            >
              <span className="material-icon">visibility_off</span>
              {pgettext("post thread", "Hidden")}
            </button>
          </li>
        )}
      </ul>
    </div>
  )
}

function getIcons(closed, hidden, pinned) {
  const icons = []
  if (pinned === 2) icons.push("bookmark")
  if (pinned === 1) icons.push("bookmark_outline")
  if (closed) icons.push("lock")
  if (hidden) icons.push("visibility_off")
  return icons
}
