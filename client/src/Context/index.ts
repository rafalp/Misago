import React from "react"
import { ICategory, IForumStats, ISettings, IUser } from "../types"
import { AuthModalContext, AuthModalProvider } from "./AuthModal"
import FormFieldContext from "./FormField"

const AuthContext = React.createContext<IUser | null>(null)
const CategoriesContext = React.createContext<Array<ICategory>>([])
const ForumStatsContext = React.createContext<IForumStats | null>(null)
const SettingsContext = React.createContext<ISettings | null>(null)

export {
  AuthContext,
  AuthModalContext,
  AuthModalProvider,
  CategoriesContext,
  FormFieldContext,
  ForumStatsContext,
  SettingsContext,
}
