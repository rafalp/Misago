import React from "react"
import { ButtonSecondary } from "../Button"
import { Paginator } from "../Paginator"
import { RootContainer } from "../Storybook"
import { Toolbar, ToolbarItem, ToolbarSeparator } from "."

export default {
  title: "UI/Toolbar",
}

export const Default = () => (
  <RootContainer>
    <Toolbar>
      <ToolbarItem>
        <Paginator page={2} pages={4} url={() => "/"} />
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
  <RootContainer>
    <Toolbar mobile>
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} block disabled />
      </ToolbarItem>
      <ToolbarSeparator />
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} block disabled />
      </ToolbarItem>
    </Toolbar>
  </RootContainer>
)

export const MobileEven = () => (
  <RootContainer>
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
  <RootContainer>
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
  <RootContainer>
    <Toolbar desktop>
      <ToolbarItem>
        <ButtonSecondary text={"Lorem ipsum"} disabled />
      </ToolbarItem>
    </Toolbar>
  </RootContainer>
)
