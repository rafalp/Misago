import classnames from "classnames"
import React from "react"
import Icon from "../Icon"

interface IPostingFormHeaderButtonProps {
  className?: string
  icon: string
  onClick?: () => void
}

const PostingFormHeaderButton: React.FC<IPostingFormHeaderButtonProps> = ({
  className,
  icon,
  onClick,
}) => (
  <button
    className={classnames("btn btn-posting-form-header btn-sm", className)}
    type="button"
    onClick={onClick}
  >
    <Icon icon={icon} fixedWidth />
  </button>
)

export default PostingFormHeaderButton
