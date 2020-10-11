import React from "react"

interface IPostingFormDialogProps {
  children: React.ReactNode
}

const PostingFormDialog: React.FC<IPostingFormDialogProps> = ({
  children,
}) => <div className="posting-form-dialog">{children}</div>

export default PostingFormDialog
