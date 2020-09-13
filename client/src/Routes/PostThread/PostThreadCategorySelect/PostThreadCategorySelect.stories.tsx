import { action } from "@storybook/addon-actions"
import React from "react"
import { ModalBody } from "../../../UI/Modal"
import { ModalContainer, categories } from "../../../UI/Storybook"
import PostThreadCategorySelectItems from "./PostThreadCategorySelectItems"
import PostThreadCategorySelectSearch from "./PostThreadCategorySelectSearch"
import useFilteredChoices from "./useFilteredChoices"

const setSearch = action("set search")
const setValue = action("set value")

export default {
  title: "Route/Post Thread/Category Select",
}

export const SelectModal = () => {
  const [search, setSearch] = React.useState<string>("")
  const filteredChoices = useFilteredChoices(categories, search)

  return (
    <ModalContainer title="Select a category">
      <PostThreadCategorySelectSearch search={search} setSearch={setSearch} />
      <PostThreadCategorySelectItems
        choices={filteredChoices}
        validChoices={filteredChoices.map((choice) => choice.id)}
        setValue={setValue}
      />
    </ModalContainer>
  )
}

export const SelectModalWithoutResults = () => {
  const [search, setSearch] = React.useState<string>("")

  return (
    <ModalContainer title="Select a category">
      <PostThreadCategorySelectSearch search={search} setSearch={setSearch} />
      <PostThreadCategorySelectItems
        choices={[]}
        validChoices={[]}
        setValue={setValue}
      />
    </ModalContainer>
  )
}

export const Search = () => (
  <ModalContainer title="Select a category">
    <PostThreadCategorySelectSearch search="" setSearch={setSearch} />
    <ModalBody>...</ModalBody>
  </ModalContainer>
)

export const SearchWithValue = () => (
  <ModalContainer title="Select a category">
    <PostThreadCategorySelectSearch
      search="Lorem ipsum"
      setSearch={setSearch}
    />
    <ModalBody>...</ModalBody>
  </ModalContainer>
)
