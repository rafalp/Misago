import React from "react"
import { RootContainer } from "../Storybook"
import { FormCheckbox } from "../Form"
import { Checkbox, CheckboxLabel } from "."

export default {
  title: "UI/Controls/Checkbox",
}

export const Default = () => (
  <RootContainer>
    <FormCheckbox>
      <Checkbox />
    </FormCheckbox>
  </RootContainer>
)

export const Checked = () => (
  <RootContainer>
    <FormCheckbox>
      <Checkbox checked />
    </FormCheckbox>
  </RootContainer>
)

export const Disabled = () => (
  <RootContainer>
    <FormCheckbox>
      <Checkbox disabled />
    </FormCheckbox>
  </RootContainer>
)

export const DisabledAndChecked = () => (
  <RootContainer>
    <FormCheckbox>
      <Checkbox checked disabled />
    </FormCheckbox>
  </RootContainer>
)

export const WithLabel = () => (
  <RootContainer>
    <FormCheckbox>
      <Checkbox id="test-checkbox" />
      <CheckboxLabel htmlFor="test-checkbox">Lorem ipsum dolor</CheckboxLabel>
    </FormCheckbox>
  </RootContainer>
)
