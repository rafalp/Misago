import React from "react"
import Anonymous from "./anonymous"
import Registered from "./registered"

export default function (props) {
  if (props.post.poster) {
    return <Registered {...props} />
  }

  return <Anonymous {...props} />
}
