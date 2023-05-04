import React from "react"

export default function DropdownFooter({ children, listItem }) {
  if (listItem) {
    return <li className="dropdown-footer">{children}</li>
  }

  return <div className="dropdown-footer">{children}</div>
}
