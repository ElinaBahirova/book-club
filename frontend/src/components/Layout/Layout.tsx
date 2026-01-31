import { Link, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import { ThemeToggle } from '../ThemeToggle'
import styles from './Layout.module.css'

export function Layout() {
  return (
    <div className={styles.layout}>
      <header className={styles.header}>
        <nav className={styles.nav}>
          <Link to="/" className={styles.logo}>
            Book Club
          </Link>
          <div className={styles.links}>
            <Link
              to="/"
              className={styles.link}
              activeProps={{ className: `${styles.link} ${styles.active}` }}
            >
              Home
            </Link>
            <Link
              to="/books"
              className={styles.link}
              activeProps={{ className: `${styles.link} ${styles.active}` }}
            >
              Books
            </Link>
          </div>
          <ThemeToggle />
        </nav>
      </header>
      <main className={styles.main}>
        <Outlet />
      </main>
      <TanStackRouterDevtools position="bottom-right" />
    </div>
  )
}
