import React from "react"

interface IPostingFormFooterProps {
  children: React.ReactNode
}

const PostingFormFooter: React.FC<IPostingFormFooterProps> = ({
  children,
}) => <div className="posting-form-footer">{children}</div>

export default PostingFormFooter
