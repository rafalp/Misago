import React from "react"

interface IPostingFormCollapsibleProps {
  children: React.ReactNode
}

const PostingFormCollapsible: React.FC<IPostingFormCollapsibleProps> = ({
  children,
}) => <div className="posting-form-collapsible">{children}</div>

export default PostingFormCollapsible
