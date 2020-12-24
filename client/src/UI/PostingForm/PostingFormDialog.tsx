import React from "react"

interface PostingFormDialogProps {
  children: React.ReactNode
}

const PostingFormDialog: React.FC<PostingFormDialogProps> = ({ children }) => (
  <div className="posting-form-dialog">{children}</div>
)

export default PostingFormDialog
