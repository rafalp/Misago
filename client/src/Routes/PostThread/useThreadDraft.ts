import React from "react"
import { getItem, setItem, removeItem } from "../../localStorage"

const TITLE = "thread_draft_title"
const MARKUP = "thread_draft_markup"
const CATEGORY = "thread_draft_category"

const useThreadDraft = () => {
  const title = React.useMemo(() => getItem(TITLE) || "", [])
  const markup = React.useMemo(() => getItem(MARKUP) || "", [])
  const category = React.useMemo(() => getItem(CATEGORY) || "", [])

  const remove = React.useCallback(() => {
    removeItem(TITLE)
    removeItem(CATEGORY)
    removeItem(MARKUP)
  }, [])

  const setTitle = React.useCallback(
    (value: string) => setItem(TITLE, value),
    []
  )

  const setCategory = React.useCallback(
    (value: string) => setItem(CATEGORY, value),
    []
  )

  const setMarkup = React.useCallback(
    (value: string) => setItem(MARKUP, value),
    []
  )

  return {
    title,
    markup,
    category,
    setTitle,
    setCategory,
    setMarkup,
    remove,
  }
}

export default useThreadDraft
