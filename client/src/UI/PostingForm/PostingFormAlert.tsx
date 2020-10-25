import React from "react"

interface IPostingFormAlertProps {
  children: React.ReactNode
}

const PostingFormAlert: React.FC<IPostingFormAlertProps> = ({ children }) => (
  <div className="posting-form-alert">
    <div className="alert alert-responsive alert-danger" role="alert">
      {children}
    </div>
  </div>
)

export default PostingFormAlert
