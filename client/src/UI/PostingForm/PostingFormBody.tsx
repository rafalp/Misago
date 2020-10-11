import React from "react"

interface IPostingFormBodyProps {
  children: React.ReactNode
}

const PostingFormBody: React.FC<IPostingFormBodyProps> = ({ children }) => (
  <div className="posting-form-body">{children}</div>
)

export default PostingFormBody
