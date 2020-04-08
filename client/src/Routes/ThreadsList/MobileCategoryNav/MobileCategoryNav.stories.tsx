import { actions } from "@storybook/addon-actions"
import React from "react"
import { CategoriesContext } from "../../../Context"
import { RootContainer, categories } from "../../../UI/Storybook"
import MobileCategoryNavButton from "./MobileCategoryNavButton"
import MobileCategoryNavModal from "./MobileCategoryNavModal"

export default {
  title: "Route/Threads/MobileCategoryNav",
}

const { open, close } = actions({ open: "open picker", close: "close picker" })

export const Button = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <MobileCategoryNavButton onClick={open} />
    </RootContainer>
  </CategoriesContext.Provider>
)

export const ButtonWithCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <MobileCategoryNavButton active={categories[0]} onClick={open} />
    </RootContainer>
  </CategoriesContext.Provider>
)

export const Modal = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer>
      <MobileCategoryNavModal isOpen={true} close={close} />
    </RootContainer>
  </CategoriesContext.Provider>
)

export const ModalWithActiveCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer>
      <MobileCategoryNavModal
        active={categories[0].id}
        isOpen={true}
        close={close}
      />
    </RootContainer>
  </CategoriesContext.Provider>
)

export const ModalWithActiveChildCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer>
      <MobileCategoryNavModal
        active={categories[0].children[1].id}
        isOpen={true}
        close={close}
      />
    </RootContainer>
  </CategoriesContext.Provider>
)
