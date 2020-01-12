import { actions } from "@storybook/addon-actions"
import { withKnobs, boolean, select, text } from "@storybook/addon-knobs"
import React from "react"
import { CardContainer, RootContainer } from "../Storybook"
import { Input } from "."

export default {
  title: "UI/Form Control",
  decorators: [withKnobs],
}

const { blur, change } = actions({ blur: "blur event", change: "change event" })

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
  const validation = select(
    "Validation state",
    {
      none: "none",
      valid: "true",
      invalid: "false",
    },
    "none"
  )

  const input = (
    <Input
      disabled={disabled}
      placeholder={placeholder}
      valid={validation !== "none" ? validation === "true" : null}
      type={type}
      onBlur={blur}
      onChange={change}
    />
  )

  return (
    <>
      <RootContainer padding>{input}</RootContainer>
      <CardContainer padding>{input}</CardContainer>
    </>
  )
}
