import React from "react"

interface PostingFormAlertProps {
  children: React.ReactNode
}

const PostingFormAlert: React.FC<PostingFormAlertProps> = ({ children }) => (
  <div className="posting-form-alert">
    <div className="alert alert-responsive alert-danger" role="alert">
      {children}
    </div>
  </div>
)

export default PostingFormAlert
