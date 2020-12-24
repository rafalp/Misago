import { withKnobs, boolean, text } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer } from "../Storybook"
import { ButtonPrimary } from "../Button"
import { Field, Form, FormFooter } from "../Form"
import Input from "../Input"
import {
  Card,
  CardAlert,
  CardBanner,
  CardBlankslate,
  CardBody,
  CardColorBand,
  CardError,
  CardFooter,
  CardFormBody,
  CardHeader,
  CardList,
  CardListItem,
  CardLoader,
  CardMessage,
} from "."

export default {
  title: "UI/Card",
  decorators: [withKnobs],
}

export const Basic = () => {
  return (
    <RootContainer>
      <Card>
        <CardBody>Lorem ipsum dolor met</CardBody>
      </Card>
    </RootContainer>
  )
}

export const HeaderAndFooter = () => {
  return (
    <RootContainer>
      <Card>
        <CardHeader title="Hello world" />
        <CardBody>Lorem ipsum dolor met</CardBody>
        <CardFooter>Do something</CardFooter>
      </Card>
    </RootContainer>
  )
}

export const WithAlert = () => {
  return (
    <RootContainer>
      <Card>
        <CardAlert>Ut malesuada interdum massa in ultrices.</CardAlert>
        <CardBody>Lorem ipsum dolor met</CardBody>
      </Card>
    </RootContainer>
  )
}

export const WithBanner = () => {
  return (
    <RootContainer>
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
        {boolean("Show alert", false) && (
          <CardAlert>Ut malesuada interdum massa in ultrices.</CardAlert>
        )}
        <CardBody>Lorem ipsum dolor met</CardBody>
      </Card>
    </RootContainer>
  )
}

export const WithColorBand = () => {
  return (
    <RootContainer>
      <Card>
        <CardColorBand color="#ff5630" />
        <CardBody>Lorem ipsum dolor met</CardBody>
      </Card>
    </RootContainer>
  )
}

export const WithColorBandBanner = () => {
  return (
    <RootContainer>
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

interface FormValues {
  username: string
  password: string
}

export const WithForm = () => {
  const title = text("Title", "Form card")
  const btnText = text("Button text", "Submit")
  const alert = boolean("Alert", false)
  const loading = boolean("Loading", false)

  return (
    <RootContainer>
      <Card>
        <CardHeader title={title} />
        <Form<FormValues>
          id="modal_form"
          defaultValues={{ username: "Bob", password: "" }}
          onSubmit={async () => {}}
        >
          {alert && (
            <CardAlert>Ut malesuada interdum massa in ultrices.</CardAlert>
          )}
          <CardFormBody>
            <Field
              label="User name or e-mail"
              name="username"
              input={<Input disabled={loading} />}
            />
            <Field
              label="Password"
              name="password"
              input={<Input disabled={loading} type="password" />}
            />
          </CardFormBody>
          <CardFooter>
            <FormFooter
              submitText={btnText}
              loading={loading}
              onCancel={() => {}}
            />
          </CardFooter>
        </Form>
      </Card>
    </RootContainer>
  )
}

export const List = () => {
  return (
    <RootContainer>
      <Card>
        <CardList>
          <CardListItem>
            Nam rhoncus ipsum non neque dapibus, sit amet condimentum est
            faucibus.
          </CardListItem>
          <CardListItem>
            Sed porttitor semper massa, sit amet ultrices velit lobortis ac.
          </CardListItem>
        </CardList>
      </Card>
    </RootContainer>
  )
}

export const ListWithLoader = () => {
  return (
    <RootContainer>
      <Card>
        <CardList>
          <CardListItem>
            Nam rhoncus ipsum non neque dapibus, sit amet condimentum est
            faucibus.
          </CardListItem>
          <CardListItem>
            Sed porttitor semper massa, sit amet ultrices velit lobortis ac.
          </CardListItem>
        </CardList>
        <CardLoader />
      </Card>
    </RootContainer>
  )
}

export const Loader = () => {
  return (
    <RootContainer>
      <Card>
        <CardLoader />
      </Card>
    </RootContainer>
  )
}

export const Blankslate = () => {
  return (
    <RootContainer>
      <Card>
        <CardBlankslate header="JohnDoe has no threads." />
      </Card>
    </RootContainer>
  )
}

export const BlankslateWithMessage = () => {
  return (
    <RootContainer>
      <Card>
        <CardBlankslate
          header="There are no threads in this category."
          message="Why not start one yourself?"
        />
      </Card>
    </RootContainer>
  )
}

export const BlankslateWithMessageAction = () => {
  return (
    <RootContainer>
      <Card>
        <CardBlankslate
          header="There are no threads in this category."
          message="Why not start one yourself?"
          actions={<ButtonPrimary text={"Start thread"} onClick={() => {}} />}
        />
      </Card>
    </RootContainer>
  )
}

export const BlankslateWithAction = () => {
  return (
    <RootContainer>
      <Card>
        <CardBlankslate
          header="There are no threads in this category."
          actions={<ButtonPrimary text={"Start thread"} onClick={() => {}} />}
        />
      </Card>
    </RootContainer>
  )
}

export const Error = () => (
  <RootContainer>
    <Card>
      <CardError header="This content is not available at the moment" />
    </Card>
  </RootContainer>
)

export const ErrorWithMessage = () => (
  <RootContainer>
    <Card>
      <CardError
        header="This content is not available."
        message={
          "It may have been moved or deleted, or you are missing permission to see it."
        }
      />
    </Card>
  </RootContainer>
)

export const Message = () => {
  return (
    <RootContainer>
      <Card>
        <CardMessage>
          <p>Lorem ipsum dolor met sit amet elit.</p>
        </CardMessage>
      </Card>
    </RootContainer>
  )
}

export const MessageWithLead = () => {
  return (
    <RootContainer>
      <Card>
        <CardMessage>
          <p className="lead">Hello world, how is it going?</p>
          <p>Lorem ipsum dolor met sit amet elit.</p>
        </CardMessage>
      </Card>
    </RootContainer>
  )
}
