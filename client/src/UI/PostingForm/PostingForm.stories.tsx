import { MockedProvider } from "@apollo/react-testing"
import { withKnobs, boolean, text } from "@storybook/addon-knobs"
import React from "react"
import * as Yup from "yup"
import { BodyScrollLockProvider } from "../../Context"
import { ButtonPrimary } from "../Button"
import Editor from "../../Editor"
import { Field, FieldError, Form } from "../Form"
import Input from "../Input"
import {
  ThreadTitleValidationError,
  ValidationError,
} from "../ValidationError"
import PostingForm from "./PostingForm"
import PostingFormAlert from "./PostingFormAlert"
import PostingFormBody from "./PostingFormBody"
import PostingFormDialog from "./PostingFormDialog"
import PostingFormFooter from "./PostingFormFooter"
import PostingFormHeader from "./PostingFormHeader"

export default {
  title: "UI/PostingForm",
  decorators: [withKnobs],
}

interface IPostingFormValues {
  title: string
  markup: string
}

const Boilerplate: React.FC = ({ children }) => {
  const [fullscreen, setFullscreen] = React.useState(false)
  const [minimized, setMinimized] = React.useState(false)

  const PostingFormSchema = Yup.object().shape({
    title: Yup.string()
      .required("value_error.thread_title.missing")
      .min(5, "value_error.any_str.min_length")
      .max(100, "value_error.any_str.max_length")
      .matches(/[a-zA-Z0-9]/, "value_error.thread_title"),
    markup: Yup.string()
      .required("value_error.missing")
      .min(5, "value_error.any_str.min_length"),
  })

  return (
    <BodyScrollLockProvider>
      <MockedProvider>
        <PostingForm
          fullscreen={fullscreen}
          minimized={minimized}
          show={boolean("Show", true)}
        >
          <PostingFormDialog>
            <Form<IPostingFormValues>
              defaultValues={{
                title: "",
                markup: "",
              }}
              disabled={boolean("Loading", false)}
              validationSchema={PostingFormSchema}
              onSubmit={async ({ clearError }) => {
                clearError()
              }}
            >
              <PostingFormHeader
                fullscreen={fullscreen}
                minimized={minimized}
                setFullscreen={setFullscreen}
                setMinimized={setMinimized}
              >
                {text("Title", "Posting form")}
              </PostingFormHeader>
              {boolean("Alert", false) && (
                <PostingFormAlert>Lorem ipsum dolor met.</PostingFormAlert>
              )}
              <PostingFormBody>{children}</PostingFormBody>
              <PostingFormFooter>
                <ButtonPrimary text="Submit" small />
              </PostingFormFooter>
            </Form>
          </PostingFormDialog>
        </PostingForm>
      </MockedProvider>
    </BodyScrollLockProvider>
  )
}

export const StartThreadForm = () => (
  <Boilerplate>
    <Field
      label="Thread title"
      name="title"
      input={<Input placeholder="Thread title" />}
      error={(error, value) => (
        <ThreadTitleValidationError
          error={error}
          value={value.trim().length}
          min={5}
          max={100}
        >
          {({ message }) => <FieldError>{message}</FieldError>}
        </ThreadTitleValidationError>
      )}
      labelReaderOnly
    />
    <Field
      label="Message contents"
      name="markup"
      className="form-group-editor"
      input={<Editor />}
      error={(error, value) => (
        <ValidationError
          error={error}
          value={value.trim().length}
          min={2}
          max={200}
        >
          {({ message }) => <FieldError>{message}</FieldError>}
        </ValidationError>
      )}
      labelReaderOnly
    />
  </Boilerplate>
)

export const ReplyForm = () => (
  <Boilerplate>
    <Field
      label="Message contents"
      name="markup"
      className="form-group-editor"
      input={<Editor />}
      error={(error, value) => (
        <ValidationError
          error={error}
          value={value.trim().length}
          min={2}
          max={200}
        >
          {({ message }) => <FieldError>{message}</FieldError>}
        </ValidationError>
      )}
      labelReaderOnly
    />
  </Boilerplate>
)
