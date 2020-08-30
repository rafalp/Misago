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
import {
  ModalContext,
  ModalConsumer,
  ModalProvider,
  useModalContext,
} from "./ModalContext"
import {
  ToastsContext,
  ToastsContextProvider,
  useToastsContext,
} from "./ToastsContext"

const AuthContext = React.createContext<IUser | null>(null)
const ForumStatsContext = React.createContext<IForumStats | null>(null)
const SettingsContext = React.createContext<ISettings | null>(null)

const useAuthContext = () => React.useContext(AuthContext)
const useForumStatsContext = () => React.useContext(ForumStatsContext)
const useSettingsContext = () => React.useContext(SettingsContext) as ISettings
const useBulkActionLimit = () => {
  const settings = React.useContext(SettingsContext)
  if (settings) return settings.bulkActionLimit
  return 2
}

export {
  AuthContext,
  AuthModalContext,
  AuthModalProvider,
  CategoriesContext,
  ForumStatsContext,
  ModalConsumer,
  ModalContext,
  ModalProvider,
  SettingsContext,
  ToastsContext,
  ToastsContextProvider,
  useAuthContext,
  useAuthModalContext,
  useBulkActionLimit,
  useCategoriesListContext,
  useCategoriesContext,
  useForumStatsContext,
  useModalContext,
  useSettingsContext,
  useToastsContext,
}
