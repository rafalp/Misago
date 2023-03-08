import React from "react"
import PostingQuoteSelection from "./PostingQuoteSelection"
import getQuoteMarkup from "./getQuoteMarkup"
import { clearGlobalState, getGlobalState, setGlobalState } from "./globalState"
import Start from "./start"
import StartPrivate from "./start-private"
import Reply from "./reply"
import Edit from "./edit"

export default function (props) {
  switch (props.mode) {
    case "START":
      return <Start {...props} />

    case "START_PRIVATE":
      return <StartPrivate {...props} />

    case "REPLY":
      return <Reply {...props} />

    case "EDIT":
      return <Edit {...props} />

    default:
      return null
  }
}

export {
  PostingQuoteSelection,
  clearGlobalState,
  getGlobalState,
  getQuoteMarkup,
  setGlobalState,
}
