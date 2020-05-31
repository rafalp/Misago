import React from "react"
import { IForumStats, ISettings, IUser } from "../types"
import {
  AuthModalContext,
  AuthModalProvider,
  useAuthModalContext,
} from "./AuthModalContext"
import {
  CategoriesContext,
  useCategoriesContext,
  useCategoriesListContext,
} from "./CategoriesContext"

const AuthContext = React.createContext<IUser | null>(null)
const ForumStatsContext = React.createContext<IForumStats | null>(null)
const SettingsContext = React.createContext<ISettings | null>(null)

const useAuthContext = () => React.useContext(AuthContext)
const useForumStatsContext = () => React.useContext(ForumStatsContext)
const useSettingsContext = () => React.useContext(SettingsContext)
const useBulkActionLimit = () => {
  const settings = React.useContext(SettingsContext)
  console.log(settings)
  if (settings) return settings.bulkActionLimit
  return 2
}

export {
  AuthContext,
  AuthModalContext,
  AuthModalProvider,
  useBulkActionLimit,
  CategoriesContext,
  ForumStatsContext,
  SettingsContext,
  useAuthContext,
  useAuthModalContext,
  useCategoriesListContext,
  useCategoriesContext,
  useForumStatsContext,
  useSettingsContext,
}
