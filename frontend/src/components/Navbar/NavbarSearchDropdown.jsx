import React from "react"
import { Dropdown } from "../Dropdown"
import { SearchDropdown } from "../Search"
import NavbarSearchToggle from "./NavbarSearchToggle"

export default function NavbarSearchDropdown({ id, className, url }) {
  return (
    <Dropdown
      id={id}
      toggle={({ isOpen, toggle }) => (
        <NavbarSearchToggle
          className={className}
          active={isOpen}
          url={url}
          onClick={(event) => {
            event.preventDefault()
            toggle()
          }}
        />
      )}
      menuClassName="search-dropdown"
      menuAlignRight
    >
      {() => <SearchDropdown />}
    </Dropdown>
  )
}
