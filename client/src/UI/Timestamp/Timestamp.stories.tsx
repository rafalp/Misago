import React from "react"
import { RootContainer } from "../Storybook"
import Timestamp from "."

export default {
  title: "UI/Timestamp",
}

export const Now = () => {
  const date = new Date()

  return (
    <RootContainer padding>
      <p>
        Now: <Timestamp date={date} />
      </p>

      <p>
        30 seconds ago:{" "}
        <Timestamp date={new Date(date.getTime() - 30 * 1000)} />
      </p>
      <p>
        5 minutes ago:{" "}
        <Timestamp date={new Date(date.getTime() - 300 * 1000)} />
      </p>
      <p>
        5 hours ago:{" "}
        <Timestamp date={new Date(date.getTime() - 5 * 3600 * 1000)} />
      </p>
      <p>
        5 days ago:{" "}
        <Timestamp date={new Date(date.getTime() - 24 * 5 * 3600 * 1000)} />
      </p>
      <p>
        7 days ago:{" "}
        <Timestamp date={new Date(date.getTime() - 24 * 7 * 3600 * 1000)} />
      </p>

      <p>
        in 30 seconds:{" "}
        <Timestamp date={new Date(date.getTime() + 30 * 1000)} />
      </p>
      <p>
        in 5 minutes:{" "}
        <Timestamp date={new Date(date.getTime() + 300 * 1000)} />
      </p>
      <p>
        in 5 hours:{" "}
        <Timestamp date={new Date(date.getTime() + 5 * 3600 * 1000)} />
      </p>
      <p>
        in 5 days:{" "}
        <Timestamp date={new Date(date.getTime() + 24 * 5 * 3600 * 1000)} />
      </p>
      <p>
        in 7 days:{" "}
        <Timestamp date={new Date(date.getTime() + 24 * 7 * 3600 * 1000)} />
      </p>
    </RootContainer>
  )
}
