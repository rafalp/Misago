import classnames from "classnames"
import React from "react"
import CategoryIcon from "../../../UI/CategoryIcon"
import Icon from "../../../UI/Icon"
import { CategoryChoiceChild } from "../PostThread.types"

interface IPostThreadCategoryInputValueProps {
  value: {
    parent?: CategoryChoiceChild | null
    child?: CategoryChoiceChild | null
  }
}

const PostThreadCategoryInputValue: React.FC<IPostThreadCategoryInputValueProps> = ({
  value,
}) => (
  <span
    className={classnames("form-control-category-select-value", {
      "form-control-category-select-value-complex": value.child,
    })}
  >
    {value.parent && (
      <span className="form-control-category-select-item">
        <CategoryIcon category={value.parent} />
        <span>{value.parent.name}</span>
      </span>
    )}
    {value.child && (
      <>
        <span className="form-control-category-select-separator">
          <Icon icon="fas fa-chevron-right" />
        </span>
        <span className="form-control-category-select-item">
          <CategoryIcon category={value.child} />
          <span>{value.child.name}</span>
        </span>
      </>
    )}
  </span>
)

export default PostThreadCategoryInputValue
