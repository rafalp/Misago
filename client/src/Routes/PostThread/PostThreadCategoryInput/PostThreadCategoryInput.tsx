import React from "react"
import { useFormContext } from "react-hook-form"
import { useModalContext } from "../../../Context"
import { useFieldContext } from "../../../UI/Form"
import { CategoryChoice } from "../PostThread.types"
import PostThreadCategorySelect from "../PostThreadCategorySelect"
import PostThreadCategoryInputBody from "./PostThreadCategoryInputBody"
import PostThreadCategoryInputPlaceholder from "./PostThreadCategoryInputPlaceholder"
import PostThreadCategoryInputValue from "./PostThreadCategoryInputValue"
import useCategoryChoice from "./useCategoryChoice"

interface PostThreadCategoryInputProps {
  choices: Array<CategoryChoice>
  validChoices: Array<string>
  responsive?: boolean
}

const PostThreadCategoryInput: React.FC<PostThreadCategoryInputProps> = ({
  choices,
  validChoices,
  responsive,
}) => {
  const context = useFieldContext()
  const { getValues, register, setValue, watch } = useFormContext()
  const { openModal } = useModalContext()
  const name = context && context.name
  const defaultValue = name ? getValues(name) : ""
  const value = name ? watch(name, defaultValue) : defaultValue

  React.useEffect(() => {
    if (name) register(name)
  }, [name, register])

  const choice = useCategoryChoice(value, choices)

  const openPicker = () => {
    openModal(
      <PostThreadCategorySelect
        choices={choices}
        validChoices={validChoices}
        setValue={(value: string) => {
          if (name) setValue(name, value)
        }}
      />
    )
  }

  return (
    <PostThreadCategoryInputBody
      disabled={context && context.disabled}
      responsive={responsive}
      onClick={openPicker}
    >
      {choice.parent ? (
        <PostThreadCategoryInputValue value={choice} />
      ) : (
        <PostThreadCategoryInputPlaceholder />
      )}
    </PostThreadCategoryInputBody>
  )
}

export default PostThreadCategoryInput
