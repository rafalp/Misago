import React from "react"
import CategoryButton from "../../../UI/CategoryButton"
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
    <CategoryButton
      category={category}
      disabled={disabled}
      nowrap
      onClick={onClick}
    />
  </div>
)

export default PostThreadCategoryInputSelected
