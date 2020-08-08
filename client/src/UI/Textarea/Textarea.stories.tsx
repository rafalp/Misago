import { actions } from "@storybook/addon-actions"
import { withKnobs, boolean, number, text } from "@storybook/addon-knobs"
import React from "react"
import { CardContainer, RootContainer } from "../Storybook"
import Textarea from "."

export default {
  title: "UI/Textarea",
  decorators: [withKnobs],
}

const { blur, change } = actions({
  blur: "blur event",
  change: "change event",
})

export const Default = () => {
  const disabled = boolean("Disabled", false)
  const placeholder = text("Placeholder", "")
  const invalid = boolean("Invalid", false)
  const rows = number("Rows", 5)

  const field = (
    <Textarea
      disabled={disabled}
      placeholder={placeholder}
      invalid={invalid}
      rows={rows > 1 ? rows : 1}
      onBlur={blur}
      onChange={change}
    />
  )

  return (
    <>
      <RootContainer padding>{field}</RootContainer>
      <CardContainer padding>{field}</CardContainer>
    </>
  )
}
