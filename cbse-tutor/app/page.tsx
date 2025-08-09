import Link from "next/link";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>CBSE Class 8 AI Tutor</h1>
        <p>
          Personalized explanations, visualizations, and practice for Class 8 Maths, Science, English, and Social Science.
        </p>
        <div className={styles.ctas}>
          <Link href="/tutor" className={styles.primary}>
            Start Learning
          </Link>
          <Link href="/subscribe" className={styles.secondary}>
            Subscribe
          </Link>
        </div>
      </main>
      <footer className={styles.footer}>
        <a href="https://cbse.gov.in/" target="_blank" rel="noopener noreferrer">
          CBSE Official
        </a>
        <a href="/privacy">Privacy</a>
        <a href="/terms">Terms</a>
      </footer>
    </div>
  );
}
