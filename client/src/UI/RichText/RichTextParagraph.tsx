import React from "react"
import { RichTextParagraph as RichTextParagraphType } from "../../types"

interface RichTextParagraphProps {
  block: RichTextParagraphType
}

const RichTextParagraph: React.FC<RichTextParagraphProps> = ({ block }) => (
  <p dangerouslySetInnerHTML={{ __html: block.text }} />
)

export default RichTextParagraph
