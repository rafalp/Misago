import React from "react"
import { CardContainer, Gallery, RootContainer } from "../Storybook"
import Button from "."

export default {
  title: "UI/Button",
}

const types = ["primary", "secondary", "success", "warning", "danger", "link"]

export const TextOnly = () => {
  const items = types.map(type => ({
    name: type,
    component: <Button text="Lorem ipsum" type={type} />,
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
  const items = types.map(type => ({
    name: type,
    component: <Button icon={"comment-alt"} type={type} />,
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
  const items = types.map(type => ({
    name: type,
    component: <Button icon={"comment-alt"} text="Start thread" type={type} />,
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
  const items = types.map(type => ({
    name: type,
    component: <Button text="Lorem ipsum" type={type} outline />,
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
  const items = types.map(type => ({
    name: type,
    component: <Button icon={"comment-alt"} type={type} outline />,
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
  const items = types.map(type => ({
    name: type,
    component: <Button icon={"comment-alt"} text="Start thread" type={type} outline />,
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
