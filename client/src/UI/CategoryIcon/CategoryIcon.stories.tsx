import React from "react"
import { RootContainer, colors, icons } from "../Storybook"
import CategoryIcon from "./CategoryIcon"

export default {
  title: "UI/CategoryIcon",
}

export const Default = () => (
  <RootContainer>
    <CategoryIcon />
  </RootContainer>
)

export const CustomColor = () => (
  <RootContainer>
    <CategoryIcon category={{ color: colors[0], icon: null }} />
  </RootContainer>
)

export const CustomIcon = () => (
  <RootContainer>
    <CategoryIcon category={{ color: null, icon: icons[0] }} />
  </RootContainer>
)

export const CustomColorAndIcon = () => (
  <RootContainer>
    <CategoryIcon category={{ color: colors[0], icon: icons[0] }} />
  </RootContainer>
)
