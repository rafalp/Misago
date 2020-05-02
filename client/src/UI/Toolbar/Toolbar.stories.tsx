import React from "react"
import { ButtonSecondary } from "../Button"
import { RootContainer } from "../Storybook"
import { Toolbar, ToolbarItem, ToolbarSeparator } from "."

export default {
  title: "UI/Toolbar",
}

export const Default = () => (
  <RootContainer padding>
    <Toolbar>
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} disabled />
      </ToolbarItem>
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} disabled />
      </ToolbarItem>
      <ToolbarSeparator />
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} disabled />
      </ToolbarItem>
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} disabled />
      </ToolbarItem>
    </Toolbar>
  </RootContainer>
)

export const Mobile = () => (
  <RootContainer padding>
    <Toolbar mobile>
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} block disabled small />
      </ToolbarItem>
      <ToolbarSeparator />
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} block disabled small />
      </ToolbarItem>
    </Toolbar>
  </RootContainer>
)

export const MobileEven = () => (
  <RootContainer padding>
    <Toolbar mobile>
      <ToolbarItem fill>
        <ButtonSecondary text={"Lorem ipsum"} block disabled small />
      </ToolbarItem>
      <ToolbarItem fill>
        <ButtonSecondary text={"Lorem ipsum"} block disabled small />
      </ToolbarItem>
      <ToolbarItem fill>
        <ButtonSecondary text={"Lorem ipsum"} block disabled small />
      </ToolbarItem>
    </Toolbar>
  </RootContainer>
)

export const Tablet = () => (
  <RootContainer padding>
    <Toolbar tablet>
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} block disabled small />
      </ToolbarItem>
      <ToolbarSeparator />
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} block disabled small />
      </ToolbarItem>
    </Toolbar>
  </RootContainer>
)

export const Desktop = () => (
  <RootContainer padding>
    <Toolbar desktop>
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} disabled />
      </ToolbarItem>
    </Toolbar>
  </RootContainer>
)
