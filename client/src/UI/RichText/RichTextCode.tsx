import classnames from "classnames"
import React from "react"
import { RichTextCode as RichTextCodeType } from "../../types"

interface RichTextCodeProps {
  block: RichTextCodeType
}

const RichTextCode: React.FC<RichTextCodeProps> = ({ block }) => (
  <div
    className={classnames(
      "rich-text-code",
      block.syntax ? "rich-text-code-" + block.syntax : ""
    )}
    data-syntax={block.syntax || ""}
  >
    <code>
      <pre>{block.text}</pre>
    </code>
  </div>
)

export default RichTextCode
