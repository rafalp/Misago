import React from "react"
import { RichTextListItem as RichTextListItemType } from "../../types"
import RichTextRenderer from "./RichTextRenderer"

interface RichTextListItemProps {
  block: RichTextListItemType
}

const RichTextListItem: React.FC<RichTextListItemProps> = ({ block }) => (
  <li>
    <RichTextRenderer richText={block.children} />
  </li>
)

export default RichTextListItem
