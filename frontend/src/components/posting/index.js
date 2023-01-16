import React from "react"
import Start from "./start"
import StartPrivate from "./start-private"
import Reply from "./reply"
import Edit from "./edit"

export default function (props) {
  if (props.mode === "START") {
    return <Start {...props} />
  } else if (props.mode === "START_PRIVATE") {
    return <StartPrivate {...props} />
  } else if (props.mode === "REPLY") {
    return <Reply {...props} />
  } else if (props.mode === "EDIT") {
    return <Edit {...props} />
  } else {
    return null
  }
}
