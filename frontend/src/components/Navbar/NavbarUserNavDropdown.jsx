import React from "react"
import { Dropdown } from "../Dropdown"
import NavbarUserNavToggle from "./NavbarUserNavToggle"
import { UserNavDropdown } from "../UserNav"

export default function NavbarUserNavDropdown({ id, className, user }) {
  return (
    <Dropdown
      id={id}
      toggle={({ isOpen, toggle }) => (
        <NavbarUserNavToggle
          className={className}
          active={isOpen}
          user={user}
          onClick={(event) => {
            event.preventDefault()
            toggle()
          }}
        />
      )}
      menuClassName="user-nav-dropdown"
      menuAlignRight
    >
      {({ isOpen, close }) => <UserNavDropdown close={close} />}
    </Dropdown>
  )
}
