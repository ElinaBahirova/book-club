import { createFileRoute } from '@tanstack/react-router'
import { z } from 'zod'
import { BookCard } from '../../components/BookCard'
import styles from './index.module.css'

const booksSearchSchema = z.object({
  search: z.string().optional(),
  sort: z.enum(['title', 'author', 'date']).optional(),
  page: z.number().int().positive().optional().default(1),
})

export const Route = createFileRoute('/books/')({
  validateSearch: booksSearchSchema,
  component: BooksPage,
})

function BooksPage() {
  const { search, sort, page } = Route.useSearch()

  // TODO: Fetch books from API using search params
  console.log('Search params:', { search, sort, page })

  const books = [
    {
      id: 1,
      title: 'The Great Gatsby',
      author: 'F. Scott Fitzgerald',
      coverUrl: 'https://books.google.com/books/content?id=iXn5U2IzVH0C&printsec=frontcover&img=1&zoom=1',
    },
    {
      id: 2,
      title: '1984',
      author: 'George Orwell',
      coverUrl: 'https://books.google.com/books/content?id=kotPYEqx7kMC&printsec=frontcover&img=1&zoom=1',
    },
  ]

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Book Collection</h1>
        <button className={styles.addButton}>+ Add Book</button>
      </div>

      <div className={styles.grid}>
        {books.map((book) => (
          <BookCard
            key={book.id}
            id={book.id}
            title={book.title}
            author={book.author}
            coverUrl={book.coverUrl}
          />
        ))}
      </div>
    </div>
  )
}
