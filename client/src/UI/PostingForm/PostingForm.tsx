import classnames from "classnames"
import React from "react"
import { BodyScrollLock } from "../../BodyScroll"

interface PostingFormProps {
  children: React.ReactNode
  fullscreen?: boolean
  minimized?: boolean
  show?: boolean
}

const PostingForm = React.forwardRef<HTMLDivElement, PostingFormProps>(
  ({ children, fullscreen, minimized, show }, ref) => (
    <div
      className={classnames("posting-form", {
        show,
        "posting-form-fullscreen": show && fullscreen,
        "posting-form-minimized": show && minimized,
        "posting-form-fixed": show && !fullscreen,
      })}
      ref={ref}
    >
      <BodyScrollLock locked={fullscreen} />
      <div className="container">{children}</div>
    </div>
  )
)

export default PostingForm
