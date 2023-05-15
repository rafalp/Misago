import React from "react"
import { Dropdown } from "../Dropdown"
import NavbarSiteNavToggle from "./NavbarSiteNavToggle"
import { SiteNavDropdown } from "../SiteNav"

export default function NavbarSiteNavDropdown({ id, className }) {
  return (
    <Dropdown
      id={id}
      toggle={({ isOpen, toggle }) => (
        <NavbarSiteNavToggle
          className={className}
          active={isOpen}
          onClick={toggle}
        />
      )}
      menuClassName="site-nav-dropdown"
      menuAlignRight
    >
      {({ isOpen, close }) => <SiteNavDropdown close={close} />}
    </Dropdown>
  )
}
