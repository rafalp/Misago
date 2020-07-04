import { action } from "@storybook/addon-actions"
import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { ButtonPrimary } from "../Button"
import { RootContainer } from "../Storybook"
import SectionLoader from "./SectionLoader"

export default {
  title: "UI/SectionLoader",
  decorators: [withKnobs],
}

export const Default = () => (
  <RootContainer padding>
    <SectionLoader>
      <p>
        Lorem ipsum dolor met <a href="/">sit amet</a> elit.
      </p>
      <p>
        <ButtonPrimary text="Test button" onClick={action("Button clicked")} />
      </p>
    </SectionLoader>
  </RootContainer>
)

export const Loading = () => (
  <RootContainer padding>
    <SectionLoader loading={true}>
      <p>
        Lorem ipsum dolor met <a href="/">sit amet</a> elit.
      </p>
      <p>
        <ButtonPrimary text="Test button" onClick={action("Button clicked")} />
      </p>
    </SectionLoader>
  </RootContainer>
)

export const Interactive = () => (
  <RootContainer padding>
    <SectionLoader loading={boolean("Loading", false)}>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
      <p>Lorem ipsum dolor met sit amet elit.</p>
    </SectionLoader>
  </RootContainer>
)
