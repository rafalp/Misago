import React from "react"
import { RichText as RichTextType } from "../../types"
import RichTextRenderer from "./RichTextRenderer"

interface RichTextProps {
  richText: RichTextType
}

const RichText: React.FC<RichTextProps> = ({ richText }) => (
  <article className="misago-rich-text">
    <RichTextRenderer richText={richText} />
  </article>
)

export default React.memo(RichText)
