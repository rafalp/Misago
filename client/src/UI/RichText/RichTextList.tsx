import React from "react"
import { RichTextList as RichTextListType } from "../../types"
import RichTextRenderer from "./RichTextRenderer"

interface RichTextListProps {
  block: RichTextListType
}

const RichTextList: React.FC<RichTextListProps> = ({ block }) =>
  block.ordered ? (
    <ol>
      <RichTextRenderer richText={block.children} />
    </ol>
  ) : (
    <ul>
      <RichTextRenderer richText={block.children} />
    </ul>
  )

export default RichTextList
