import React from "react"
import { RootContainer, colors, icons } from "../Storybook"
import CategoryIcon from "./CategoryIcon"

export default {
  title: "UI/CategoryIcon",
}

export const Default = () => (
  <RootContainer padding>
    <CategoryIcon />
  </RootContainer>
)

export const CustomColor = () => (
  <RootContainer padding>
    <CategoryIcon category={{ color: colors[0], icon: null }} />
  </RootContainer>
)

export const CustomIcon = () => (
  <RootContainer padding>
    <CategoryIcon category={{ color: null, icon: icons[0] }} />
  </RootContainer>
)

export const CustomColorAndIcon = () => (
  <RootContainer padding>
    <CategoryIcon category={{ color: colors[0], icon: icons[0] }} />
  </RootContainer>
)
