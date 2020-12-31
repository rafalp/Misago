import React from "react"
import { RichTextQuote as RichTextQuoteType } from "../../types"
import RichTextRenderer from "./RichTextRenderer"

interface RichTextQuoteProps {
  block: RichTextQuoteType
}

const RichTextQuote: React.FC<RichTextQuoteProps> = ({ block }) => (
  <div className="rich-text-quote">
    <blockquote data-block="quote">
      <RichTextRenderer richText={block.children} />
    </blockquote>
  </div>
)

export default RichTextQuote
