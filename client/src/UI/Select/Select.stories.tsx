import { actions } from "@storybook/addon-actions"
import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { CardContainer, RootContainer } from "../Storybook"
import Select from "."

export default {
  title: "UI/Select",
  decorators: [withKnobs],
}

const { blur, change } = actions({
  blur: "blur event",
  change: "change event",
})

export const SelectInput = () => {
  const disabled = boolean("Disabled", false)
  const invalid = boolean("Invalid", false)

  const field = (
    <Select
      disabled={disabled}
      invalid={invalid}
      options={[
        {
          value: 1,
          name: "First option",
        },
        {
          value: 2,
          name: "Second option",
        },
      ]}
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
