import { createFileRoute, Link } from '@tanstack/react-router'
import { z } from 'zod'
import styles from './route.module.css'

const bookParamsSchema = z.object({
  bookId: z.string().regex(/^\d+$/, 'Book ID must be a number'),
})

export const Route = createFileRoute('/books/$bookId')({
  params: {
    parse: (params) => bookParamsSchema.parse(params),
    stringify: (params) => params,
  },
  component: BookDetailPage,
})

function BookDetailPage() {
  const { bookId } = Route.useParams()

  // TODO: Fetch book details from API
  const book = {
    id: bookId,
    title: 'The Great Gatsby',
    author: 'F. Scott Fitzgerald',
    description: 'A story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.',
    coverUrl: 'https://books.google.com/books/content?id=iXn5U2IzVH0C&printsec=frontcover&img=1&zoom=1',
    publishedDate: '1925',
    pageCount: 180,
    categories: 'Fiction, Classics',
  }

  return (
    <div className={styles.container}>
      <Link to="/books" className={styles.backLink}>
        ← Back to Books
      </Link>

      <div className={styles.content}>
        <div className={styles.coverWrapper}>
          <img src={book.coverUrl} alt={book.title} className={styles.cover} />
        </div>

        <div className={styles.details}>
          <div>
            <h1 className={styles.title}>{book.title}</h1>
            <p className={styles.author}>by {book.author}</p>
          </div>

          <p className={styles.description}>{book.description}</p>

          <div className={styles.meta}>
            <span>📅 {book.publishedDate}</span>
            <span>📖 {book.pageCount} pages</span>
            <span>🏷️ {book.categories}</span>
          </div>

          <div className={styles.actions}>
            <button className={styles.primaryButton}>Set as Current Pick</button>
            <button className={styles.secondaryButton}>Remove from Club</button>
          </div>
        </div>
      </div>
    </div>
  )
}
