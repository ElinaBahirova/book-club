import { Link } from '@tanstack/react-router'
import styles from './BookCard.module.css'

interface BookCardProps {
  id: number
  title: string
  author: string
  coverUrl: string
}

export function BookCard({ id, title, author, coverUrl }: BookCardProps) {
  return (
    <Link
      to="/books/$bookId"
      params={{ bookId: String(id) }}
      className={styles.card}
    >
      <div className={styles.coverWrapper}>
        <img src={coverUrl} alt={title} className={styles.cover} />
      </div>
      <div className={styles.info}>
        <h3 className={styles.title}>{title}</h3>
        <p className={styles.author}>{author}</p>
      </div>
    </Link>
  )
}
