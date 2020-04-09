import React from "react"
import { RootContainer } from "../Storybook"
import { Card, CardBanner, CardBody, CardColorBand, CardFooter, CardHeader } from "."

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

export const WithBanner = () => {
  return (
    <RootContainer padding>
      <Card>
        <CardBanner
          align="center"
          background="#2c3e50"
          height={100}
          url="http://lorempixel.com/1280/200/"
        />
        <CardBanner
          align="center"
          background="#2c3e50"
          height={100}
          url="http://lorempixel.com/1536/200/"
          mobile
        />
        <CardBody>Lorem ipsum dolor met</CardBody>
      </Card>
    </RootContainer>
  )
}

export const WithColorBand = () => {
  return (
    <RootContainer padding>
      <Card>
        <CardColorBand color="#ff5630" />
        <CardBody>Lorem ipsum dolor met</CardBody>
      </Card>
    </RootContainer>
  )
}

export const WithColorBandBanner = () => {
  return (
    <RootContainer padding>
      <Card>
        <CardColorBand color="#ff5630" />
        <CardBanner
          align="center"
          background="#2c3e50"
          height={100}
          url="http://lorempixel.com/1280/200/"
        />
        <CardBanner
          align="center"
          background="#2c3e50"
          height={100}
          url="http://lorempixel.com/1536/200/"
          mobile
        />
        <CardBody>Lorem ipsum dolor met</CardBody>
      </Card>
    </RootContainer>
  )
}