export interface IThreadToolbarProps {
  page?: {
    number: number
    pagination: {
      pages: number
    }
  } | null
  paginatorUrl: (page: number) => string
}
