import React from "react"
import {
  CardContainer,
  Gallery,
  RootContainer,
  userFactory,
} from "../Storybook"
import Avatar from "."

export default {
  title: "UI/Avatar",
}

export const UserAvatar = () => {
  const user = userFactory()
  const items = [200, 100, 64, 32, 16].map((size) => ({
    name: `${size} x ${size}`,
    component: <Avatar size={size} user={user} />,
  }))

  return (
    <>
      <RootContainer nopadding>
        <Gallery items={items} />
      </RootContainer>
      <CardContainer nopadding>
        <Gallery items={items} />
      </CardContainer>
    </>
  )
}

export const BlankAvatar = () => {
  const items = [200, 100, 64, 32, 16].map((size) => ({
    name: `${size} x ${size}`,
    component: <Avatar size={size} />,
  }))

  return (
    <>
      <RootContainer nopadding>
        <Gallery items={items} />
      </RootContainer>
      <CardContainer nopadding>
        <Gallery items={items} />
      </CardContainer>
    </>
  )
}
