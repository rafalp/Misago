import React from "react"
import { RootContainer } from "../Storybook"
import { Card, CardBody, CardFooter, CardHeader } from "."

export default {
  title: "UI/Card",
}

export const Basic = () => {
  return (
    <RootContainer padding>
      <Card>
        <CardBody>Lorem ipsum dolor met</CardBody>
      </Card>
    </RootContainer>
  )
}

export const HeaderAndFooter = () => {
  return (
    <RootContainer padding>
      <Card>
        <CardHeader title="Hello world" />
        <CardBody>Lorem ipsum dolor met</CardBody>
        <CardFooter>Do something</CardFooter>
      </Card>
    </RootContainer>
  )
}