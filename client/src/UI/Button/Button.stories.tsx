import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { CardContainer, Matrix, RootContainer } from "../Storybook"
import { Button, ButtonType } from "."

export default {
  title: "UI/Button",
  decorators: [withKnobs],
}

const blockKnob = () => boolean("Block", false)

const types = [
  ButtonType.PRIMARY,
  ButtonType.SECONDARY,
  ButtonType.SUCCESS,
  ButtonType.WARNING,
  ButtonType.DANGER,
  ButtonType.LINK,
]

export const TextOnly = () => {
  const block = blockKnob()
  const items = types.map((type) => [
    {
      name: type,
      component: <Button block={block} text="Lorem ipsum" type={type} />,
    },
    {
      name: type + " loading",
      component: (
        <Button block={block} text="Lorem ipsum" type={type} loading />
      ),
    },
    {
      name: type + " disabled",
      component: (
        <Button block={block} text="Lorem ipsum" type={type} disabled />
      ),
    },
  ])

  return (
    <>
      <RootContainer>
        <Matrix items={items} />
      </RootContainer>
      <CardContainer>
        <Matrix items={items} />
      </CardContainer>
    </>
  )
}

export const OutlinedTextOnly = () => {
  const block = blockKnob()
  const items = types.map((type) => [
    {
      name: type,
      component: (
        <Button block={block} text="Lorem ipsum" type={type} outline />
      ),
    },
    {
      name: type + " loading",
      component: (
        <Button block={block} text="Lorem ipsum" type={type} loading outline />
      ),
    },
    {
      name: type + " disabled",
      component: (
        <Button
          block={block}
          text="Lorem ipsum"
          type={type}
          disabled
          outline
        />
      ),
    },
  ])

  return (
    <>
      <RootContainer>
        <Matrix items={items} />
      </RootContainer>
      <CardContainer>
        <Matrix items={items} />
      </CardContainer>
    </>
  )
}

export const IconOnly = () => {
  const block = blockKnob()
  const items = types.map((type) => [
    {
      name: type,
      component: <Button block={block} icon={"comment-alt"} type={type} />,
    },
    {
      name: type + " loading",
      component: (
        <Button block={block} icon={"comment-alt"} type={type} loading />
      ),
    },
    {
      name: type + " disabled",
      component: (
        <Button block={block} icon={"comment-alt"} type={type} disabled />
      ),
    },
  ])

  return (
    <>
      <RootContainer>
        <Matrix items={items} />
      </RootContainer>
      <CardContainer>
        <Matrix items={items} />
      </CardContainer>
    </>
  )
}

export const OutlinedIconOnly = () => {
  const block = blockKnob()
  const items = types.map((type) => [
    {
      name: type,
      component: (
        <Button block={block} icon={"comment-alt"} type={type} outline />
      ),
    },
    {
      name: type + " loading",
      component: (
        <Button
          block={block}
          icon={"comment-alt"}
          type={type}
          loading
          outline
        />
      ),
    },
    {
      name: type + " disabled",
      component: (
        <Button
          block={block}
          icon={"comment-alt"}
          type={type}
          disabled
          outline
        />
      ),
    },
  ])

  return (
    <>
      <RootContainer>
        <Matrix items={items} />
      </RootContainer>
      <CardContainer>
        <Matrix items={items} />
      </CardContainer>
    </>
  )
}

export const IconAndText = () => {
  const block = blockKnob()
  const items = types.map((type) => [
    {
      name: type,
      component: (
        <Button
          block={block}
          icon={"comment-alt"}
          text="Start thread"
          type={type}
        />
      ),
    },
    {
      name: type + " loading",
      component: (
        <Button
          block={block}
          icon={"comment-alt"}
          text="Start thread"
          type={type}
          loading
        />
      ),
    },
    {
      name: type + " disabled",
      component: (
        <Button
          block={block}
          icon={"comment-alt"}
          text="Start thread"
          type={type}
          disabled
        />
      ),
    },
  ])

  return (
    <>
      <RootContainer>
        <Matrix items={items} />
      </RootContainer>
      <CardContainer>
        <Matrix items={items} />
      </CardContainer>
    </>
  )
}

export const OutlinedIconAndText = () => {
  const block = blockKnob()
  const items = types.map((type) => [
    {
      name: type,
      component: (
        <Button
          block={block}
          icon={"comment-alt"}
          text="Start thread"
          type={type}
          outline
        />
      ),
    },
    {
      name: type + " loading",
      component: (
        <Button
          block={block}
          icon={"comment-alt"}
          text="Start thread"
          type={type}
          loading
          outline
        />
      ),
    },
    {
      name: type + " disabled",
      component: (
        <Button
          block={block}
          icon={"comment-alt"}
          text="Start thread"
          type={type}
          disabled
          outline
        />
      ),
    },
  ])

  return (
    <>
      <RootContainer>
        <Matrix items={items} />
      </RootContainer>
      <CardContainer>
        <Matrix items={items} />
      </CardContainer>
    </>
  )
}
