import React from "react"
import portal from "../../../UI/portal"

interface IThreadReplySpacerProps {
  height: number
}

const ThreadReplySpacer: React.FC<IThreadReplySpacerProps> = ({ height }) => {
  return portal(<div style={{ height }} />)
}

export default ThreadReplySpacer
