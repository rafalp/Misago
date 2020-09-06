import { action } from "@storybook/addon-actions"
import React from "react"
import { RootContainer, categories } from "../../../UI/Storybook"
import PostThreadCategoryInputBody from "./PostThreadCategoryInputBody"
import PostThreadCategoryInputEmpty from "./PostThreadCategoryInputEmpty"
import PostThreadCategoryInputSelected from "./PostThreadCategoryInputSelected"

const openPicker = action("open modal with categories")

export default {
  title: "Route/Post Thread/Category Input",
}

export const Empty = () => (
  <RootContainer padding>
    <PostThreadCategoryInputBody>
      <PostThreadCategoryInputEmpty onClick={openPicker} />
    </PostThreadCategoryInputBody>
  </RootContainer>
)

export const EmptyDisabled = () => (
  <RootContainer padding>
    <PostThreadCategoryInputBody>
      <PostThreadCategoryInputEmpty onClick={openPicker} disabled />
    </PostThreadCategoryInputBody>
  </RootContainer>
)

export const Category = () => (
  <RootContainer padding>
    <PostThreadCategoryInputBody>
      <PostThreadCategoryInputSelected
        category={categories[0]}
        onClick={openPicker}
      />
    </PostThreadCategoryInputBody>
  </RootContainer>
)

export const CategoryDisabled = () => (
  <RootContainer padding>
    <PostThreadCategoryInputBody>
      <PostThreadCategoryInputSelected
        category={categories[0]}
        onClick={openPicker}
        disabled
      />
    </PostThreadCategoryInputBody>
  </RootContainer>
)

export const ChildCategory = () => (
  <RootContainer padding>
    <PostThreadCategoryInputBody>
      <PostThreadCategoryInputSelected
        category={categories[0]}
        onClick={openPicker}
      />
      <PostThreadCategoryInputSelected
        category={categories[3]}
        onClick={openPicker}
      />
    </PostThreadCategoryInputBody>
  </RootContainer>
)

export const ChildCategoryDisabled = () => (
  <RootContainer padding>
    <PostThreadCategoryInputBody>
      <PostThreadCategoryInputSelected
        category={categories[0]}
        onClick={openPicker}
        disabled
      />
      <PostThreadCategoryInputSelected
        category={categories[3]}
        onClick={openPicker}
        disabled
      />
    </PostThreadCategoryInputBody>
  </RootContainer>
)
