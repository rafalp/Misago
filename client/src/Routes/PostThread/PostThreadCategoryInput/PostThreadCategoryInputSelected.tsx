import React from "react"
import CategoryIcon from "../../../UI/CategoryIcon"
import { ICategoryChoiceChild } from "../PostThread.types"

interface IPostThreadCategoryInputSelectedProps {
  category: ICategoryChoiceChild
  disabled?: boolean
  onClick: () => void
}

const PostThreadCategoryInputSelected: React.FC<IPostThreadCategoryInputSelectedProps> = ({
  category,
  disabled,
  onClick,
}) => (
  <div className="form-control-category">
    <button
      className="btn btn-secondary btn-responsive"
      type="button"
      disabled={disabled}
      onClick={onClick}
    >
      <CategoryIcon category={category} />
      <span>{category.name}</span>
    </button>
  </div>
)

export default PostThreadCategoryInputSelected
