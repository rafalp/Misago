import React from "react"
import Icon from "../Icon"
import { RootContainer, categories } from "../Storybook"
import CategoryButton from "./CategoryButton"

export default {
  title: "UI/CategoryButton",
}

export const Button = () => (
  <RootContainer padding>
    <CategoryButton category={categories[0]} />
  </RootContainer>
)

export const Link = () => (
  <RootContainer padding>
    <CategoryButton category={categories[0]} link="/" />
  </RootContainer>
)

export const NoWrapExtraIcon = () => (
  <RootContainer padding>
    <CategoryButton
      category={categories[0]}
      icon={<Icon icon="far fa-plus-square" />}
      nowrap
    />
  </RootContainer>
)
