import React from "react"
import { RichTextHorizontalRule as RichTextHorizontalRuleType } from "../../types"

interface RichTextHorizontalRuleProps {
  block: RichTextHorizontalRuleType
}

const RichTextHorizontalRule: React.FC<RichTextHorizontalRuleProps> = ({
  block,
}) => <hr />

export default RichTextHorizontalRule
