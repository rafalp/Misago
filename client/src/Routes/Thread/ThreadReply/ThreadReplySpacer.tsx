import React from "react"
import portal from "../../../UI/portal"

interface ThreadReplySpacerProps {
  height: number
}

const ThreadReplySpacer: React.FC<ThreadReplySpacerProps> = ({ height }) => {
  return portal(<div style={{ height }} />)
}

export default ThreadReplySpacer
