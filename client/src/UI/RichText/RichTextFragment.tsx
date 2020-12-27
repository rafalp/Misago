import React from "react"
import { RichTextFragment as RichTextFragmentType } from "../../types"

interface RichTextFragmentProps {
  block: RichTextFragmentType
}

const RichTextFragment: React.FC<RichTextFragmentProps> = ({ block }) => (
  <span dangerouslySetInnerHTML={{ __html: block.text }} />
)

export default RichTextFragment
