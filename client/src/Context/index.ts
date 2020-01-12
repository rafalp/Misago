import React from "react"
import { ICategory, ISettings, IUser } from "../types"
import { AuthModalContext, AuthModalProvider } from "./AuthModal"
import FormFieldContext from "./FormField"

const AuthContext = React.createContext<IUser | null>(null)
const CategoriesContext = React.createContext<Array<ICategory>>([])
const SettingsContext = React.createContext<ISettings | null>(null)

export {
  AuthContext,
  AuthModalContext,
  AuthModalProvider,
  CategoriesContext,
  FormFieldContext,
  SettingsContext,
}
