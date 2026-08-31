# Responsive UI Pitfalls (Next.js & Tailwind)

When transitioning a desktop-first design to mobile (e.g. Next.js SaaS landing pages):
- **Horizontal Scroll Bug:** Always add `overflow-x-hidden` to the main container (e.g., `<main className="overflow-x-hidden">`) to prevent right-side empty space when user swipes horizontally.
- **Line-Break Mismatches:** Avoid hard `<br className="hidden md:block" />` which can force unnatural wrapping on mobile. Rely on responsive padding, `max-w` constraints, and responsive typography (e.g., `text-4xl sm:text-5xl`).
- **Fat Finger Buttons:** Ensure mobile CTA buttons span the full width (`w-full sm:w-auto`) for easier tapping.
- **Card Sizing & Overflow:** For glassmorphic or fixed-width cards (e.g., Chat Mockups), use `max-w-[85%]` or `max-w-md` on mobile instead of fixed pixels. Use `truncate` or `break-words` on dynamic text fields inside flex layouts to prevent long names from breaking the flex container boundary.
- **Heavy Transforms:** Disable 3D perspective transforms (`perspective`, `rotate-x`) on mobile viewports as they consume too much screen real estate and cause touch rendering issues. Apply them conditionally (e.g., `md:transform md:rotate-x-12`).