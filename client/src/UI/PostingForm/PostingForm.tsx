import classnames from "classnames"
import React from "react"

interface IPostingFormProps {
  children: React.ReactNode
  fullscreen?: boolean
  minimized?: boolean
  show?: boolean
  element?: React.RefObject<HTMLDivElement>
}

const PostingForm: React.FC<IPostingFormProps> = ({
  children,
  fullscreen,
  minimized,
  show,
  element,
}) => (
  <div
    className={classnames("posting-form", {
      show,
      "posting-form-fullscreen": show && fullscreen,
      "posting-form-minimized": show && minimized,
      "posting-form-overlaid": show && !fullscreen,
    })}
    ref={element}
  >
    <div className="container">{children}</div>
  </div>
)

export default PostingForm
