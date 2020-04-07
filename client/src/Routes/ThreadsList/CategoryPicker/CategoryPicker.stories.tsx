import { actions } from "@storybook/addon-actions"
import React from "react"
import { CategoriesContext } from "../../../Context"
import { RootContainer, categories } from "../../../UI/Storybook"
import CategoryPickerButton from "./CategoryPickerButton"
import CategoryPickerModal from "./CategoryPickerModal"

export default {
  title: "Route/Threads/CategoryPicker",
}

const { open, close } = actions({ open: "open picker", close: "close picker" })

export const Button = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <CategoryPickerButton onClick={open} />
    </RootContainer>
  </CategoriesContext.Provider>
)

export const ButtonWithCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <CategoryPickerButton active={categories[0]} onClick={open} />
    </RootContainer>
  </CategoriesContext.Provider>
)

export const Modal = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer>
      <CategoryPickerModal isOpen={true} close={close} />
    </RootContainer>
  </CategoriesContext.Provider>
)

export const ModalWithActiveCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer>
      <CategoryPickerModal
        active={categories[1]}
        isOpen={true}
        close={close}
      />
    </RootContainer>
  </CategoriesContext.Provider>
)

export const ModalWithActiveChildCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer>
      <CategoryPickerModal
        active={categories[0].children[1]}
        isOpen={true}
        close={close}
      />
    </RootContainer>
  </CategoriesContext.Provider>
)
