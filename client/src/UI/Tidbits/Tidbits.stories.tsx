import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { CardContainer, categories, userFactory } from "../Storybook"
import {
  TidbitActivityLastReply,
  TidbitActivityStart,
  TidbitAvatar,
  TidbitCategory,
  TidbitClosed,
  TidbitItem,
  TidbitMembers,
  TidbitPosts,
  TidbitReplies,
  TidbitThreads,
  TidbitTimestamp,
  TidbitUser,
  Tidbits,
} from "."

export default {
  title: "UI/Tidbits",
  decorators: [withKnobs],
}

const smallKnob = () => boolean("Small", false)
const verticalKnob = () => boolean("Vertical", false)

export const Item = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnob()}>
      <TidbitItem>Lorem ipsum</TidbitItem>
      <TidbitItem>Dolor met</TidbitItem>
    </Tidbits>
  </CardContainer>
)

export const Numerical = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnob()}>
      <TidbitPosts value={142567} />
      <TidbitReplies value={431413} />
      <TidbitThreads value={1089524} />
      <TidbitMembers value={25663} />
    </Tidbits>
  </CardContainer>
)

export const Categories = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnob()}>
      <TidbitCategory category={categories[0]} parent />
      <TidbitCategory category={categories[2]} />
    </Tidbits>
  </CardContainer>
)

export const CategoriesDisabled = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnob()}>
      <TidbitCategory category={categories[0]} disabled parent />
      <TidbitCategory category={categories[2]} disabled />
    </Tidbits>
  </CardContainer>
)

export const Timestamps = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnob()}>
      <TidbitTimestamp date={new Date("2020-05-02T12:10:41.159Z")} />
      <TidbitTimestamp date={new Date("2020-05-02T12:10:41.159Z")} url="#" />
    </Tidbits>
  </CardContainer>
)

export const User = () => {
  const small = smallKnob()
  const user = userFactory({ slug: "aerith", name: "Aerith" })

  return (
    <CardContainer padding>
      <Tidbits small={small} vertical={verticalKnob()}>
        <TidbitAvatar user={user} />
        <TidbitUser user={user} />
      </Tidbits>
    </CardContainer>
  )
}

export const UserAnonymous = () => {
  const small = smallKnob()

  return (
    <CardContainer padding>
      <Tidbits small={small} vertical={verticalKnob()}>
        <TidbitAvatar />
        <TidbitUser name="Aerith" />
      </Tidbits>
    </CardContainer>
  )
}

export const Closed = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnob()}>
      <TidbitClosed />
    </Tidbits>
  </CardContainer>
)

export const Activity = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnob()}>
      <TidbitActivityStart
        userName="Aerith"
        date={new Date("2020-05-02T12:10:41.159Z")}
      />
      <TidbitActivityStart
        user={{ id: "1", slug: "aerith", name: "Aerith" }}
        userName="Aerith"
        date={new Date("2020-05-02T12:10:41.159Z")}
      />
      <TidbitActivityStart
        userName="Aerith"
        date={new Date("2020-05-02T12:10:41.159Z")}
        url="#"
      />
      <TidbitActivityStart
        user={{ id: "1", slug: "aerith", name: "Aerith" }}
        userName="Aerith"
        date={new Date("2020-05-02T12:10:41.159Z")}
        url="#"
      />
      <TidbitActivityLastReply
        userName="Aerith"
        date={new Date("2020-05-02T12:10:41.159Z")}
      />
      <TidbitActivityLastReply
        user={{ id: "1", slug: "aerith", name: "Aerith" }}
        userName="Aerith"
        date={new Date("2020-05-02T12:10:41.159Z")}
      />
      <TidbitActivityLastReply
        userName="Aerith"
        date={new Date("2020-05-02T12:10:41.159Z")}
        url="#"
      />
      <TidbitActivityLastReply
        user={{ id: "1", slug: "aerith", name: "Aerith" }}
        userName="Aerith"
        date={new Date("2020-05-02T12:10:41.159Z")}
        url="#"
      />
    </Tidbits>
  </CardContainer>
)
