import React from "react"
import { getItem, setItem, removeItem } from "../../../localStorage"

const useNewReplyDraft = (threadId: string) => {
  const key = "thread_reply_draft_markup" + threadId

  const getDraft = React.useCallback(() => getItem(key) || "", [key])
  const setDraft = React.useCallback(
    (value: string) => {
      if (value.trim().length > 0) {
        setItem(key, value)
      }
    },
    [key]
  )
  const removeDraft = React.useCallback(() => removeItem(key), [key])

  return {
    getDraft,
    setDraft,
    removeDraft,
  }
}

export default useNewReplyDraft
