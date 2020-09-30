import React from "react"
import { CardContainer } from "../Storybook"
import PageTitle from "./PageTitle"

export default {
  title: "UI/PageTitle",
}

export const Title = () => (
  <CardContainer>
    <PageTitle text="Misago forums" />
  </CardContainer>
)
