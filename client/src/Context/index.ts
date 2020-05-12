import React from "react"
import { ICategory, IForumStats, ISettings, IUser } from "../types"
import { AuthModalContext, AuthModalProvider } from "./AuthModal"
import FormFieldContext from "./FormField"

const AuthContext = React.createContext<IUser | null>(null)
const CategoriesContext = React.createContext<Array<ICategory>>([])
const ForumStatsContext = React.createContext<IForumStats | null>(null)
const SettingsContext = React.createContext<ISettings | null>(null)

const useAuthContext = () => React.useContext(AuthContext)
const useCategoriesContext = () => React.useContext(CategoriesContext)
const useCategoriesListContext = () => {
  const categories = useCategoriesContext()
  return React.useMemo(() => {
    const choices: Array<{ category: ICategory; depth: number }> = []
    categories.forEach((category) => {
      choices.push({ category, depth: 0 })
      category.children.forEach((child) =>
        choices.push({ category: child, depth: 1 })
      )
    })
    return choices
  }, [categories])
}

export {
  AuthContext,
  AuthModalContext,
  AuthModalProvider,
  CategoriesContext,
  FormFieldContext,
  ForumStatsContext,
  SettingsContext,
  useAuthContext,
  useCategoriesListContext,
  useCategoriesContext,
}
