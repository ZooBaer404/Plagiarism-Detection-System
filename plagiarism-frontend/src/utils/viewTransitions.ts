export function startViewTransition() {
  if (document.startViewTransition) {
    document.startViewTransition(() => {});
  }
}