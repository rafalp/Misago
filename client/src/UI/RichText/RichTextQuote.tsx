import React from "react"
import { RichTextQuote as RichTextQuoteType } from "../../types"
import RichTextQuoteHeader from "./RichTextQuoteHeader"
import RichTextRenderer from "./RichTextRenderer"

interface RichTextQuoteProps {
  block: RichTextQuoteType
}

const RichTextQuote: React.FC<RichTextQuoteProps> = ({ block }) => (
  <div className="rich-text-quote">
    {block.author && (
      <RichTextQuoteHeader author={block.author} post={block.post} />
    )}
    <blockquote
      data-block="quote"
      data-author={block.author ? block.author.name : null}
      data-post={block.post || null}
    >
      <RichTextRenderer richText={block.children} />
    </blockquote>
  </div>
)

export default RichTextQuote
