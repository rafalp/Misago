import { actions } from "@storybook/addon-actions"
import React from "react"
import { CategoriesContext } from "../../../Context"
import {
  RootContainer,
  SettingsContextFactory,
  categories,
} from "../../../UI/Storybook"
import ThreadsCategoriesModal from "./ThreadsCategoriesModal"
import ThreadsCategoriesModalButton from "./ThreadsCategoriesModalButton"
import { ThreadsCategoriesModalContext } from "./ThreadsCategoriesModalContext"

export default {
  title: "Route/Threads/ThreadsCategoriesModal",
}

const { open, close } = actions({ open: "open picker", close: "close picker" })

export const Button = () => (
  <CategoriesContext.Provider value={categories}>
    <ThreadsCategoriesModalContext.Provider
      value={{ open, close, isOpen: false }}
    >
      <RootContainer>
        <ThreadsCategoriesModalButton />
      </RootContainer>
    </ThreadsCategoriesModalContext.Provider>
  </CategoriesContext.Provider>
)

export const ButtonWithCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <ThreadsCategoriesModalContext.Provider
      value={{ open, close, isOpen: false }}
    >
      <RootContainer>
        <ThreadsCategoriesModalButton
          active={{ category: categories[0], parent: categories[0] }}
        />
      </RootContainer>
    </ThreadsCategoriesModalContext.Provider>
  </CategoriesContext.Provider>
)

export const Modal = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <ThreadsCategoriesModalContext.Provider
        value={{ open, close, isOpen: true }}
      >
        <RootContainer>
          <ThreadsCategoriesModal />
        </RootContainer>
      </ThreadsCategoriesModalContext.Provider>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)

export const ModalWithActiveCategory = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <ThreadsCategoriesModalContext.Provider
        value={{
          open,
          close,
          active: { category: categories[0], parent: categories[0] },
          isOpen: true,
        }}
      >
        <RootContainer>
          <ThreadsCategoriesModal />
        </RootContainer>
      </ThreadsCategoriesModalContext.Provider>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)

export const ModalWithActiveChildCategory = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <ThreadsCategoriesModalContext.Provider
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
          <ThreadsCategoriesModal />
        </RootContainer>
      </ThreadsCategoriesModalContext.Provider>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)
