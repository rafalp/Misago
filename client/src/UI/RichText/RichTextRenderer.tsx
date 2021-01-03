import React from "react"
import { RichText as RichTextType } from "../../types"
import RICH_TEXT_BLOCKS from "./blocks"

interface RichTextRendererProps {
  richText: RichTextType
}

const RichTextRenderer: React.FC<RichTextRendererProps> = ({ richText }) => (
  <>
    {richText.map((block, index) => {
      if (RICH_TEXT_BLOCKS[block.type]) {
        const Component = RICH_TEXT_BLOCKS[block.type]
        return <Component key={block.id} block={block} index={index + 1} />
      }

      return null
    })}
  </>
)

export default RichTextRenderer
