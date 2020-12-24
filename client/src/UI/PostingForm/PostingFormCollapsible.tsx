import React from "react"

interface PostingFormCollapsibleProps {
  children: React.ReactNode
}

const PostingFormCollapsible: React.FC<PostingFormCollapsibleProps> = ({
  children,
}) => <div className="posting-form-collapsible">{children}</div>

export default PostingFormCollapsible
