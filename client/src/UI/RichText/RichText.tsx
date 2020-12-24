import React from "react"
import { RichText as RichTextType } from "../../types"

interface RichTextProps {
  richText: RichTextType
}

const RichText: React.FC<RichTextProps> = ({ richText }) => (
  <article className="misago-richtext">
    {richText.map((block) => {
      if (block.type === "p") {
        return (
          <p key={block.id} dangerouslySetInnerHTML={{ __html: block.text }} />
        )
      }

      return null
    })}
  </article>
)

export default RichText
