import React from "react"
import CategoryButton from "../../../UI/CategoryButton"
import {
  CategoriesListGroup,
  CategoriesListGroupItem,
} from "../../../UI/CategoriesListGroup"
import { ModalBody } from "../../../UI/Modal"
import { CategoryChoice } from "../PostThread.types"

interface IPostThreadCategorySelectItemsProps {
  choices: Array<CategoryChoice>
  validChoices: Array<string>
  setValue: (value: string) => void
}

const PostThreadCategorySelectItems: React.FC<IPostThreadCategorySelectItemsProps> = ({
  choices,
  validChoices,
  setValue,
}) => (
  <ModalBody className="category-select-items">
    <CategoriesListGroup>
      {choices.map((category) => (
        <CategoriesListGroupItem key={category.id}>
          <CategoryButton
            category={category}
            disabled={validChoices.indexOf(category.id) < 0}
            responsive
            onClick={() => setValue(category.id)}
          />
          {category.children.length > 0 && (
            <CategoriesListGroup>
              {category.children.map((child) => (
                <CategoriesListGroupItem key={child.id}>
                  <CategoryButton
                    category={child}
                    disabled={validChoices.indexOf(child.id) < 0}
                    responsive
                    onClick={() => setValue(child.id)}
                  />
                </CategoriesListGroupItem>
              ))}
            </CategoriesListGroup>
          )}
        </CategoriesListGroupItem>
      ))}
    </CategoriesListGroup>
  </ModalBody>
)

export default PostThreadCategorySelectItems
