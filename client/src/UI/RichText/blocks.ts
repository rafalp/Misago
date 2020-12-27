import React from "react"
import RichTextCode from "./RichTextCode"
import RichTextFragment from "./RichTextFragment"
import RichTextHeader from "./RichTextHeader"
import RichTextHorizontalRule from "./RichTextHorizontalRule"
import RichTextList from "./RichTextList"
import RichTextListItem from "./RichTextListItem"
import RichTextParagraph from "./RichTextParagraph"
import RichTextQuote from "./RichTextQuote"

const RICH_TEXT_BLOCKS: Record<string, React.ComponentType<any>> = {
  code: RichTextCode,
  f: RichTextFragment,
  h1: RichTextHeader,
  h2: RichTextHeader,
  h3: RichTextHeader,
  h4: RichTextHeader,
  h5: RichTextHeader,
  h6: RichTextHeader,
  hr: RichTextHorizontalRule,
  li: RichTextListItem,
  list: RichTextList,
  p: RichTextParagraph,
  quote: RichTextQuote,
}

export default RICH_TEXT_BLOCKS
