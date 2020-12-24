import React from "react"
import { CategoriesContext } from "../../Context"
import { Field, Form } from "../Form"
import { CardContainer, categories } from "../Storybook"
import CategorySelect from "."

export default {
  title: "UI/CategorySelect",
}

interface FormValues {
  category?: string
}

export const CategorySelectInput = () => (
  <CategoriesContext.Provider value={categories}>
    <Form<FormValues> id="category_select_field" onSubmit={() => {}}>
      <CardContainer>
        <Field
          label="Select category"
          name="category"
          input={<CategorySelect />}
        />
      </CardContainer>
    </Form>
  </CategoriesContext.Provider>
)
