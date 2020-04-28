import { action } from "@storybook/addon-actions"
import React from "react"
import { ButtonPrimary } from "../Button"
import { CardContainer, RootContainer } from "../Storybook"
import Dropdown from "./Dropdown"
import DropdownButton from "./DropdownButton"
import DropdownDivider from "./DropdownDivider"
import DropdownLink from "./DropdownLink"

export default {
  title: "UI/Dropdown",
}

const click = action("button click")

export const Default = () => (
  <>
    <RootContainer center padding>
      <Dropdown
        toggle={({ ref, toggle }) => (
          <ButtonPrimary elementRef={ref} text="Toggle" onClick={toggle} />
        )}
        menu={<Menu />}
      />
    </RootContainer>
    <CardContainer center padding>
      <Dropdown
        toggle={({ ref, toggle }) => (
          <ButtonPrimary elementRef={ref} text="Toggle" onClick={toggle} />
        )}
        menu={<Menu />}
      />
    </CardContainer>
  </>
)

export const MenuItems = () => (
  <RootContainer padding>
    <div className="dropdown-menu d-block position-static">
      <DropdownLink to="/">Private messages</DropdownLink>
      <DropdownButton
        icon="sign-in-alt"
        text="Log in"
        onClick={click}
        iconSolid
      />
      <DropdownButton icon="key" text="Sign up" onClick={click} iconSolid />
      <DropdownButton text="Subscribe" onClick={click} loading />
      <DropdownDivider />
      <DropdownButton text="Plain item" onClick={click} />
    </div>
  </RootContainer>
)

const Menu = () => (
  <>
    <DropdownButton text="Example item" onClick={click} />
  </>
)
