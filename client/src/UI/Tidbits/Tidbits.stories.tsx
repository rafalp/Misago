import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { CardContainer, categories } from "../Storybook"
import {
  TidbitActivityLastReply,
  TidbitActivityStart,
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
const verticalKnow = () => boolean("Vertical", false)

export const Item = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnow()}>
      <TidbitItem>Lorem ipsum</TidbitItem>
      <TidbitItem>Dolor met</TidbitItem>
    </Tidbits>
  </CardContainer>
)

export const Numerical = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnow()}>
      <TidbitPosts value={142567} />
      <TidbitReplies value={431413} />
      <TidbitThreads value={1089524} />
      <TidbitMembers value={25663} />
    </Tidbits>
  </CardContainer>
)

export const Categories = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnow()}>
      <TidbitCategory category={categories[0]} parent />
      <TidbitCategory category={categories[2]} />
    </Tidbits>
  </CardContainer>
)

export const Timestamps = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnow()}>
      <TidbitTimestamp date={new Date("2020-05-02T12:10:41.159Z")} />
      <TidbitTimestamp date={new Date("2020-05-02T12:10:41.159Z")} url="#" />
    </Tidbits>
  </CardContainer>
)

export const User = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnow()}>
      <TidbitUser user={{ id: "1", slug: "aerith", name: "Aerith" }} />
      <TidbitUser name="Aerith" />
    </Tidbits>
  </CardContainer>
)

export const Closed = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnow()}>
      <TidbitClosed />
    </Tidbits>
  </CardContainer>
)

export const Activity = () => (
  <CardContainer padding>
    <Tidbits small={smallKnob()} vertical={verticalKnow()}>
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
