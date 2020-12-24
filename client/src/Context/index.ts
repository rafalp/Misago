import React from "react"
import { AuthUser, ForumStats, Settings } from "../types"
import {
  AuthModalContext,
  AuthModalProvider,
  useAuthModalContext,
} from "./AuthModalContext"
import {
  BodyScrollLockContext,
  BodyScrollLockProvider,
  useBodyScrollLockContext,
} from "./BodyScrollLockContext"
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
  ToastsProvider,
  useToastsContext,
} from "./ToastsContext"

const AuthContext = React.createContext<AuthUser | null>(null)
const ForumStatsContext = React.createContext<ForumStats | null>(null)
const SettingsContext = React.createContext<Settings | null>(null)

const useAuthContext = () => React.useContext(AuthContext)
const useForumStatsContext = () => React.useContext(ForumStatsContext)
const useSettingsContext = () => {
  const settings = React.useContext(SettingsContext)
  if (settings === null) {
    throw new Error("useSettingsContext() used outside of settings provider!")
  }
  return settings
}
const useBulkActionLimit = () => {
  const settings = React.useContext(SettingsContext)
  if (settings) return settings.bulkActionLimit
  return 2
}

export {
  AuthContext,
  AuthModalContext,
  AuthModalProvider,
  BodyScrollLockContext,
  BodyScrollLockProvider,
  CategoriesContext,
  ForumStatsContext,
  ModalConsumer,
  ModalContext,
  ModalProvider,
  SettingsContext,
  ToastsContext,
  ToastsProvider,
  useAuthContext,
  useAuthModalContext,
  useBodyScrollLockContext,
  useBulkActionLimit,
  useCategoriesListContext,
  useCategoriesContext,
  useForumStatsContext,
  useModalContext,
  useSettingsContext,
  useToastsContext,
}
