import React from "react"
import { Route } from "react-router-dom"
import * as urls from "../../urls"
import AllThreadsList from "./AllThreadsList"
import { CategoryPickerModal } from "./CategoryPicker"
import CategoryThreadsList from "./CategoryThreadsList"

interface ICategoriesModalState {
  isOpen: boolean
  active: { id: string } | null
}

const ThreadsList: React.FC = () => {
  const [{ active, isOpen }, setState] = React.useState<ICategoriesModalState>(
    {
      active: null,
      isOpen: false,
    }
  )
  const open = (active?: { id: string } | null) => {
    setState({ isOpen: true, active: active || null })
  }
  const close = () => setState({ isOpen: false, active: null })

  return (
    <>
      <CategoryPickerModal active={active} close={close} isOpen={isOpen} />
      <Route
        path={urls.category({ id: ":id", slug: ":slug" })}
        render={() => <CategoryThreadsList openCategoryPicker={open} />}
        exact
      />
      <Route
        path="/"
        render={() => <AllThreadsList openCategoryPicker={open} />}
        exact
      />
    </>
  )
}

export default ThreadsList
