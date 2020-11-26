import React from "react"

interface IPostingFormErrorProps {
  detail?: React.ReactNode
  error: React.ReactNode
}

const PostingFormError: React.FC<IPostingFormErrorProps> = ({
  detail,
  error,
}) => (
  <div className="posting-form-error">
    <div className="posting-form-error-body">
      <div className="posting-form-error-icon" />
      <div className="posting-form-error-message">
        <p className="lead">{error}</p>
        {detail && <p>{detail}</p>}
      </div>
    </div>
  </div>
)

export default PostingFormError
