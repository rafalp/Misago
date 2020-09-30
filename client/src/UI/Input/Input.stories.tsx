import { actions } from "@storybook/addon-actions"
import { withKnobs, boolean, select, text } from "@storybook/addon-knobs"
import React from "react"
import { CardContainer, RootContainer } from "../Storybook"
import Input from "."

export default {
  title: "UI/Controls/Input",
  decorators: [withKnobs],
}

const { blur, change } = actions({
  blur: "blur event",
  change: "change event",
})

export const TextInput = () => {
  const disabled = boolean("Disabled", false)
  const placeholder = text("Placeholder", "")
  const type = select(
    "Type",
    {
      text: "text",
      password: "password",
      email: "email",
    },
    "text"
  )
  const invalid = boolean("Invalid", false)

  const field = (
    <Input
      disabled={disabled}
      placeholder={placeholder}
      invalid={invalid}
      type={type}
      onBlur={blur}
      onChange={change}
    />
  )

  return (
    <>
      <RootContainer>{field}</RootContainer>
      <CardContainer>{field}</CardContainer>
    </>
  )
}
