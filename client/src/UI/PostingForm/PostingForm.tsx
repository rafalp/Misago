import classnames from "classnames"
import React from "react"

interface IPostingFormProps {
  children: React.ReactNode
  fullscreen?: boolean
  minimized?: boolean
  show?: boolean
}

const PostingForm = React.forwardRef<HTMLDivElement, IPostingFormProps>(
  ({ children, fullscreen, minimized, show }, ref) => (
    <div
      className={classnames("posting-form", {
        show,
        "posting-form-fullscreen": show && fullscreen,
        "posting-form-minimized": show && minimized,
        "posting-form-overlaid": show && !fullscreen,
      })}
      ref={ref}
    >
      <div className="container">{children}</div>
    </div>
  )
)

export default PostingForm
