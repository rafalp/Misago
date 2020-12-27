import React from "react"
import { RichTextHeader as RichTextHeaderType } from "../../types"

interface RichTextHeaderProps {
  block: RichTextHeaderType
}

const RichTextHeader: React.FC<RichTextHeaderProps> = ({ block }) => {
  if (block.type === "h1") {
    return <h1 dangerouslySetInnerHTML={{ __html: block.text }} />
  }

  if (block.type === "h2") {
    return <h2 dangerouslySetInnerHTML={{ __html: block.text }} />
  }

  if (block.type === "h3") {
    return <h3 dangerouslySetInnerHTML={{ __html: block.text }} />
  }

  if (block.type === "h4") {
    return <h4 dangerouslySetInnerHTML={{ __html: block.text }} />
  }

  if (block.type === "h5") {
    return <h5 dangerouslySetInnerHTML={{ __html: block.text }} />
  }

  if (block.type === "h6") {
    return <h6 dangerouslySetInnerHTML={{ __html: block.text }} />
  }

  return null
}

export default RichTextHeader
