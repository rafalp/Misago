import React from "react"
import PageTitle from "./PageTitle"
import { CardContainer } from "../Storybook"

export default {
  title: "UI/PageTitle",
}

export const Title = () => (
  <CardContainer padding>
    <PageTitle text="Misago forums" />
  </CardContainer>
)
