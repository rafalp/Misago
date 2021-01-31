import React from "react"
import { RichTextHeader as RichTextHeaderType } from "../../types"

interface RichTextHeaderProps {
  block: RichTextHeaderType
}

const RichTextHeader: React.FC<RichTextHeaderProps> = ({ block }) => (
  <div
    className={block.type}
    data-block={block.type.toUpperCase()}
    dangerouslySetInnerHTML={{ __html: block.text }}
  />
)

export default RichTextHeader
