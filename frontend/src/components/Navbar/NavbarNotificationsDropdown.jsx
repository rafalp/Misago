import React from "react"
import { Dropdown } from "../Dropdown"
import NotificationsDropdown from "../NotificationsDropdown"
import NavbarNotificationsToggle from "./NavbarNotificationsToggle"

export default function NavbarNotificationsDropdown({
  id,
  className,
  badge,
  url,
}) {
  return (
    <Dropdown
      id={id}
      toggle={({ isOpen, toggle }) => (
        <NavbarNotificationsToggle
          className={className}
          active={isOpen}
          badge={badge}
          url={url}
          onClick={(event) => {
            event.preventDefault()
            toggle()
          }}
        />
      )}
      menuClassName="notifications-dropdown"
      menuAlignRight
    >
      {({ isOpen }) => <NotificationsDropdown active={isOpen} />}
    </Dropdown>
  )
}
