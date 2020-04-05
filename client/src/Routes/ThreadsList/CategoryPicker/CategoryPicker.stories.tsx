import { action } from "@storybook/addon-actions"
import React from "react"
import { CategoriesContext } from "../../../Context"
import { RootContainer, categories } from "../../../UI/Storybook"
import CategoryPicker from "./CategoryPickerButton"

export default {
  title: "Route/Threads/CategoryPicker",
}

const open = action("open picker")

export const ButtonDefault = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <CategoryPicker onClick={open} />
    </RootContainer>
  </CategoriesContext.Provider>
)

export const ButtonWithCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <CategoryPicker active={categories[0]} onClick={open} />
    </RootContainer>
  </CategoriesContext.Provider>
)
