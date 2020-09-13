import React from "react"
import { useFormContext } from "react-hook-form"
import { useModalContext } from "../../../Context"
import { useFieldContext } from "../../../UI/Form"
import { ICategoryChoice } from "../PostThread.types"
import PostThreadCategorySelect from "../PostThreadCategorySelect"
import PostThreadCategoryInputBody from "./PostThreadCategoryInputBody"
import PostThreadCategoryInputEmpty from "./PostThreadCategoryInputEmpty"
import PostThreadCategoryInputSelected from "./PostThreadCategoryInputSelected"
import useCategoryChoice from "./useCategoryChoice"

interface IPostThreadCategoryInputProps {
  choices: Array<ICategoryChoice>
  validChoices: Array<string>
}

const PostThreadCategoryInput: React.FC<IPostThreadCategoryInputProps> = ({
  choices,
  validChoices,
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
          if (name) setValue(name, value, true)
        }}
      />
    )
  }

  if (choice.parent) {
    return (
      <PostThreadCategoryInputBody>
        <PostThreadCategoryInputSelected
          category={choice.parent}
          disabled={context && context.disabled}
          onClick={openPicker}
        />
        {choice.child && (
          <PostThreadCategoryInputSelected
            category={choice.child}
            disabled={context && context.disabled}
            onClick={openPicker}
          />
        )}
      </PostThreadCategoryInputBody>
    )
  }

  return (
    <PostThreadCategoryInputBody>
      <PostThreadCategoryInputEmpty
        disabled={context && context.disabled}
        onClick={openPicker}
      />
    </PostThreadCategoryInputBody>
  )
}

export default PostThreadCategoryInput
