import React from "react"
import CategoryButton from "../CategoryButton"
import { Layout, LayoutSide } from "../Layout"
import { ModalBody } from "../Modal"
import { ModalContainer, RootContainer, categories } from "../Storybook"
import CategoriesListGroup from "./CategoriesListGroup"
import CategoriesListGroupItem from "./CategoriesListGroupItem"

export default {
  title: "UI/CategoriesListGroup",
}

export const SideNav = () => (
  <RootContainer>
    <Layout>
      <LayoutSide>
        <CategoriesListGroup>
          {categories.map((category) => (
            <CategoriesListGroupItem key={category.id}>
              <CategoryButton category={category} />
              {category.children.length > 0 && (
                <CategoriesListGroup>
                  {category.children.map((child) => (
                    <CategoriesListGroupItem key={child.id}>
                      <CategoryButton category={child} />
                    </CategoriesListGroupItem>
                  ))}
                </CategoriesListGroup>
              )}
            </CategoriesListGroupItem>
          ))}
        </CategoriesListGroup>
      </LayoutSide>
    </Layout>
  </RootContainer>
)

export const InModal = () => (
  <ModalContainer>
    <ModalBody>
      <CategoriesListGroup>
        {categories.map((category) => (
          <CategoriesListGroupItem key={category.id}>
            <CategoryButton category={category} responsive />
            {category.children.length > 0 && (
              <CategoriesListGroup>
                {category.children.map((child) => (
                  <CategoriesListGroupItem key={child.id}>
                    <CategoryButton category={child} responsive />
                  </CategoriesListGroupItem>
                ))}
              </CategoriesListGroup>
            )}
          </CategoriesListGroupItem>
        ))}
      </CategoriesListGroup>
    </ModalBody>
  </ModalContainer>
)
