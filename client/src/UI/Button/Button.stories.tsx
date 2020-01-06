import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { CardContainer, Gallery, RootContainer } from "../Storybook"
import Button from "."

export default {
  title: "UI/Button",
  decorators: [withKnobs],
}

const types = ["primary", "secondary", "success", "warning", "danger", "link"]

export const TextOnly = () => {
  const disabled = boolean("Disabled", false)

  const items = types.map(type => ({
    name: type,
    component: <Button text="Lorem ipsum" type={type} disabled={disabled} />,
  }))

  return (
    <>
      <RootContainer>
        <Gallery items={items} />
      </RootContainer>
      <CardContainer>
        <Gallery items={items} />
      </CardContainer>
    </>
  )
}

export const IconOnly = () => {
  const disabled = boolean("Disabled", false)

  const items = types.map(type => ({
    name: type,
    component: <Button icon={"comment-alt"} type={type} disabled={disabled} />,
  }))

  return (
    <>
      <RootContainer>
        <Gallery items={items} />
      </RootContainer>
      <CardContainer>
        <Gallery items={items} />
      </CardContainer>
    </>
  )
}

export const IconAndText = () => {
  const disabled = boolean("Disabled", false)

  const items = types.map(type => ({
    name: type,
    component: (
      <Button icon={"comment-alt"} text="Start thread" type={type} disabled={disabled} />
    ),
  }))

  return (
    <>
      <RootContainer>
        <Gallery items={items} />
      </RootContainer>
      <CardContainer>
        <Gallery items={items} />
      </CardContainer>
    </>
  )
}
export const OutlineTextOnly = () => {
  const disabled = boolean("Disabled", false)

  const items = types.map(type => ({
    name: type,
    component: <Button text="Lorem ipsum" type={type} disabled={disabled} outline />,
  }))

  return (
    <>
      <RootContainer>
        <Gallery items={items} />
      </RootContainer>
      <CardContainer>
        <Gallery items={items} />
      </CardContainer>
    </>
  )
}

export const OutlineIconOnly = () => {
  const disabled = boolean("Disabled", false)

  const items = types.map(type => ({
    name: type,
    component: <Button icon={"comment-alt"} type={type} disabled={disabled} outline />,
  }))

  return (
    <>
      <RootContainer>
        <Gallery items={items} />
      </RootContainer>
      <CardContainer>
        <Gallery items={items} />
      </CardContainer>
    </>
  )
}

export const OutlineIconAndText = () => {
  const disabled = boolean("Disabled", false)

  const items = types.map(type => ({
    name: type,
    component: (
      <Button icon={"comment-alt"} text="Start thread" type={type} disabled={disabled} outline />
    ),
  }))

  return (
    <>
      <RootContainer>
        <Gallery items={items} />
      </RootContainer>
      <CardContainer>
        <Gallery items={items} />
      </CardContainer>
    </>
  )
}
