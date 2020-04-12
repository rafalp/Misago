import React from "react"
import {
  CategoriesNav,
  Layout,
  LayoutMain,
  LayoutSide,
  RouteContainer,
} from "../../UI"
import { MobileCategoryNavButton } from "./MobileCategoryNav"
import { IThreadsProps, IActiveCategory } from "./Threads.types"

interface IThreadsLayoutProps extends IThreadsProps {
  category?: IActiveCategory | null
  className?: string
  children: React.ReactNode
}

const ThreadsLayout: React.FC<IThreadsLayoutProps> = ({
  category,
  className,
  children,
  openCategoryPicker
}) => (
  <RouteContainer className={className}>
    <Layout>
      <LayoutSide>
        <CategoriesNav active={category} />
      </LayoutSide>
      <LayoutMain>
        <MobileCategoryNavButton
          active={category?.category}
          onClick={() => openCategoryPicker(category)}
        />
        {children}
      </LayoutMain>
    </Layout>
  </RouteContainer>
)

export default ThreadsLayout
