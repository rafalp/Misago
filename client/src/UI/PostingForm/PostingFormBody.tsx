import React from "react"

interface PostingFormBodyProps {
  children: React.ReactNode
}

const PostingFormBody: React.FC<PostingFormBodyProps> = ({ children }) => (
  <div className="posting-form-body">{children}</div>
)

export default PostingFormBody
