import React from "react"
import { Dropdown } from "../Dropdown"
import { SearchDropdown } from "../search"
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

            window.setTimeout(() => {
              document
                .querySelector(".search-dropdown .form-control-search")
                .focus()
            }, 0)
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
