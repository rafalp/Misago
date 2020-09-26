import React from "react"
import Icon from "../../../UI/Icon"

interface IPostThreadCategoryInputBodyProps {
  children: React.ReactNode
  disabled?: boolean
  onClick: () => void
}

const PostThreadCategoryInputBody: React.FC<IPostThreadCategoryInputBodyProps> = ({
  children,
  disabled,
  onClick,
}) => (
  <button
    className="form-control form-control-category-select"
    type="button"
    disabled={disabled}
    onClick={onClick}
  >
    {children}
    <span className="form-control-category-select-caret">
      <Icon icon="fas fa-ellipsis-v" />
    </span>
  </button>
)

export default PostThreadCategoryInputBody
