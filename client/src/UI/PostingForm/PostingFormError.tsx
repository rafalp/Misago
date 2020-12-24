import React from "react"

interface PostingFormErrorProps {
  detail?: React.ReactNode
  error: React.ReactNode
}

const PostingFormError: React.FC<PostingFormErrorProps> = ({
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
