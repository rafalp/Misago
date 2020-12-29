import React from "react"
import { RichText as RichTextType } from "../../types"
import RichTextRenderer from "./RichTextRenderer"

interface RichTextProps {
  author?: string
  postId?: string
  richText: RichTextType
}

const RichText: React.FC<RichTextProps> = ({ author, postId, richText }) => (
  <article
    className="misago-rich-text"
    data-author={author}
    data-post={postId}
  >
    <RichTextRenderer richText={richText} />
  </article>
)

export default React.memo(RichText)
