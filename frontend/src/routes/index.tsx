import { createFileRoute, Link } from '@tanstack/react-router'
import { FeatureCard } from '../components/FeatureCard'
import styles from './index.module.css'

export const Route = createFileRoute('/')({
  component: HomePage,
})

function HomePage() {
  return (
    <div className={styles.container}>
      <section className={styles.hero}>
        <h1 className={styles.title}>
          Welcome to <span className={styles.highlight}>Book Club</span>
        </h1>
        <p className={styles.subtitle}>
          Discover and discuss great books with your community. Curate your collection and share your reading journey.
        </p>
        <Link to="/books" className={styles.cta}>
          Browse Books
        </Link>
      </section>

      <section className={styles.features}>
        <FeatureCard
          icon="📚"
          title="Curated Collection"
          description="Hand-picked books from Google Books API for meaningful discussions."
        />
        <FeatureCard
          icon="💬"
          title="Community Discussions"
          description="Share thoughts and engage with fellow book lovers."
        />
        <FeatureCard
          icon="⭐"
          title="Current Picks"
          description="See what the club is reading this month."
        />
      </section>
    </div>
  )
}
