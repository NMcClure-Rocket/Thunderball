export default function Footer() {
  return (
    <footer
      style={{
        backgroundColor: 'var(--color-primary)',
        borderTop: '3px solid var(--color-secondary)',
        color: 'var(--color-text-on-dark)',
        padding: '12px 20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
    >
      <span style={{ fontSize: '0.85rem', color: 'var(--color-text-on-dark)', opacity: 0.8 }}>
        &copy; 2026 Spellstack. All rights reserved.
      </span>
      <a
        href="http://127.0.0.1:8001"
        target="_blank"
        rel="noreferrer"
        style={{ color: 'var(--color-highlight)', textDecoration: 'underline', fontWeight: 600 }}
      >
        Documents
      </a>
    </footer>
  );
}
