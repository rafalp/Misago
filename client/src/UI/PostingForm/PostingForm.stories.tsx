import { MockedProvider } from "@apollo/react-testing"
import { withKnobs, boolean, text } from "@storybook/addon-knobs"
import React from "react"
import * as Yup from "yup"
import { BodyScrollLockProvider } from "../../Context"
import Editor from "../../Editor"
import { ButtonPrimary } from "../Button"
import { Field, FieldError, Form } from "../Form"
import { categories } from "../Storybook"
import { ValidationError } from "../ValidationError"
import PostingForm from "./PostingForm"
import PostingFormAlert from "./PostingFormAlert"
import PostingFormBody from "./PostingFormBody"
import PostingFormCollapsible from "./PostingFormCollapsible"
import PostingFormDialog from "./PostingFormDialog"
import PostingFormError from "./PostingFormError"
import PostingFormHeader from "./PostingFormHeader"
import PostingFormLoader from "./PostingFormLoader"

export default {
  title: "UI/PostingForm",
  decorators: [withKnobs],
}

interface IPostingFormValues {
  title: string
  category: string
  markup: string
}

const Boilerplate: React.FC = ({ children }) => {
  const [fullscreen, setFullscreen] = React.useState(false)
  const [minimized, setMinimized] = React.useState(false)

  const PostingFormSchema = Yup.object().shape({
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
                category: categories[0].children[0].id,
                markup: "",
              }}
              disabled={boolean("Loading", false)}
              validationSchema={PostingFormSchema}
              onSubmit={async ({ clearError }) => {
                clearError()
              }}
            >
              <PostingFormBody>
                <PostingFormHeader
                  fullscreen={fullscreen}
                  minimized={minimized}
                  setFullscreen={setFullscreen}
                  setMinimized={setMinimized}
                >
                  {text("Title", "Posting form")}
                </PostingFormHeader>
                <PostingFormCollapsible>
                  {boolean("Alert", false) && (
                    <PostingFormAlert>Lorem ipsum dolor met.</PostingFormAlert>
                  )}
                  {children}
                </PostingFormCollapsible>
              </PostingFormBody>
            </Form>
          </PostingFormDialog>
        </PostingForm>
      </MockedProvider>
    </BodyScrollLockProvider>
  )
}

export const Reply = () => (
  <Boilerplate>
    <Field
      label="Message contents"
      name="markup"
      className="form-group-editor"
      input={<Editor submit={<ButtonPrimary text="Submit" small />} />}
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

export const Loading = () => (
  <Boilerplate>
    <PostingFormLoader />
  </Boilerplate>
)

export const Error = () => (
  <Boilerplate>
    <PostingFormError
      error="Reply form could not be loaded at this time."
      detail="An unexpected error has occurred."
    />
  </Boilerplate>
)
