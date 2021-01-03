import React from "react"
import { RichTextListItem as RichTextListItemType } from "../../types"
import RichTextRenderer from "./RichTextRenderer"

interface RichTextListItemProps {
  block: RichTextListItemType
  index: number
}

const RichTextListItem: React.FC<RichTextListItemProps> = ({
  block,
  index,
}) => (
  <li data-index={index}>
    <RichTextRenderer richText={block.children} />
  </li>
)

export default RichTextListItem
