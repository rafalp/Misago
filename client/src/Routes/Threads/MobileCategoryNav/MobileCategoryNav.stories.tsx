import { actions } from "@storybook/addon-actions"
import React from "react"
import { CategoriesContext } from "../../../Context"
import { RootContainer, categories } from "../../../UI/Storybook"
import { ThreadsCategoryModalContext } from "../ThreadsCategoryModalContext"
import MobileCategoryNavButton from "./MobileCategoryNavButton"
import MobileCategoryNavModal from "./MobileCategoryNavModal"

export default {
  title: "Route/Threads/MobileCategoryNav",
}

const { open, close } = actions({ open: "open picker", close: "close picker" })

export const Button = () => (
  <CategoriesContext.Provider value={categories}>
    <ThreadsCategoryModalContext.Provider
      value={{ open, close, isOpen: false }}
    >
      <RootContainer padding>
        <MobileCategoryNavButton />
      </RootContainer>
    </ThreadsCategoryModalContext.Provider>
  </CategoriesContext.Provider>
)

export const ButtonWithCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <ThreadsCategoryModalContext.Provider
      value={{ open, close, isOpen: false }}
    >
      <RootContainer padding>
        <MobileCategoryNavButton
          active={{ category: categories[0], parent: categories[0] }}
        />
      </RootContainer>
    </ThreadsCategoryModalContext.Provider>
  </CategoriesContext.Provider>
)

export const Modal = () => (
  <CategoriesContext.Provider value={categories}>
    <ThreadsCategoryModalContext.Provider
      value={{ open, close, isOpen: true }}
    >
      <RootContainer>
        <MobileCategoryNavModal />
      </RootContainer>
    </ThreadsCategoryModalContext.Provider>
  </CategoriesContext.Provider>
)

export const ModalWithActiveCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <ThreadsCategoryModalContext.Provider
      value={{
        open,
        close,
        active: { category: categories[0], parent: categories[0] },
        isOpen: true,
      }}
    >
      <RootContainer>
        <MobileCategoryNavModal />
      </RootContainer>
    </ThreadsCategoryModalContext.Provider>
  </CategoriesContext.Provider>
)

export const ModalWithActiveChildCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <ThreadsCategoryModalContext.Provider
      value={{
        open,
        close,
        active: {
          category: categories[0].children[1],
          parent: categories[0],
        },
        isOpen: true,
      }}
    >
      <RootContainer>
        <MobileCategoryNavModal />
      </RootContainer>
    </ThreadsCategoryModalContext.Provider>
  </CategoriesContext.Provider>
)
