import React from "react"
import { ICategory, IRegisterModalContext, ISettings, IUser } from "./types"

const { Consumer: AuthConsumer, Provider: AuthProvider } = React.createContext<IUser | null>(null)
const { Consumer: CategoriesConsumer, Provider: CategoriesProvider } = React.createContext<
  Array<ICategory>
>([])
const { Consumer: SettingsConsumer, Provider: SettingsProvider } = React.createContext<ISettings | null>(null)

const { Consumer: RegisterModalConsumer, Provider: RegisterModalProvider } = React.createContext<IRegisterModalContext>({
  isOpen: false,
  openModal: () => {},
  closeModal: () => {},
})

export {
  AuthConsumer,
  AuthProvider,
  CategoriesConsumer,
  CategoriesProvider,
  RegisterModalConsumer,
  RegisterModalProvider,
  SettingsConsumer,
  SettingsProvider,
}
