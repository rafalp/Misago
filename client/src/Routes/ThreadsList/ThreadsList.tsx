import React from "react"
import { Route } from "react-router-dom"
import * as urls from "../../urls"
import AllThreadsList from "./AllThreadsList"
import { MobileCategoryNavModal } from "./MobileCategoryNav"
import CategoryThreadsList from "./CategoryThreadsList"
import { IActiveCategory } from "./ThreadsList.types"

interface ICategoriesModalState {
  isOpen: boolean
  active?: IActiveCategory | null
}

const ThreadsList: React.FC = () => {
  const [{ active, isOpen }, setState] = React.useState<ICategoriesModalState>(
    {
      active: null,
      isOpen: false,
    }
  )
  const open = (active?: IActiveCategory | null) => {
    setState({ isOpen: true, active: active || null })
  }
  const close = () => setState({ isOpen: false, active: null })

  return (
    <>
      <MobileCategoryNavModal active={active} close={close} isOpen={isOpen} />
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
