import { action } from "@storybook/addon-actions"
import React from "react"
import { ButtonPrimary } from "../Button"
import { CardContainer, RootContainer } from "../Storybook"
import Dropdown from "./Dropdown"
import DropdownButton from "./DropdownButton"
import DropdownContainer from "./DropdownContainer"
import DropdownDivider from "./DropdownDivider"
import DropdownHeader from "./DropdownHeader"
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
        menu={() => <Menu />}
      />
    </RootContainer>
    <CardContainer center padding>
      <Dropdown
        toggle={({ ref, toggle }) => (
          <ButtonPrimary elementRef={ref} text="Toggle" onClick={toggle} />
        )}
        menu={() => <Menu />}
      />
    </CardContainer>
  </>
)

export const MenuItems = () => (
  <RootContainer padding>
    <div className="dropdown-menu d-block position-static">
      <DropdownHeader text="Example menu" />
      <DropdownLink text="Private messages" to="/" />
      <DropdownButton
        icon="far fa-sign-in-alt"
        text="Log in"
        onClick={click}
      />
      <DropdownButton icon="key" text="Sign up" onClick={click} />
      <DropdownButton text="Subscribe" onClick={click} loading />
      <DropdownDivider />
      <DropdownButton text="Plain item" onClick={click} />
      <DropdownContainer>Extra content in container.</DropdownContainer>
    </div>
  </RootContainer>
)

const Menu = () => (
  <>
    <DropdownHeader text="Example menu" />
    <DropdownButton text="Example item" onClick={click} />
    <DropdownDivider />
    <DropdownButton text="Example item" onClick={click} />
    <DropdownContainer>Extra content in container.</DropdownContainer>
  </>
)
