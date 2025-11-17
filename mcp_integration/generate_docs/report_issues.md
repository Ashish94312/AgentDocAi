# Open Issues in Vercel Next.js Repository

## Relevant Open Issues

1. **[not-found.tsx: Infinite Loop when a Component Calls router.refresh](https://github.com/vercel/next.js/issues/86197)**
   - **User:** columk1
   - **Created At:** 2025-11-17
   - **Labels:** Not Found
   - **Summary:** This issue describes an infinite loop occurring when a 404 error is triggered within a layout and `router.refresh` is called. The user reports that this leads to repeated 404 requests.

2. **[Docs: Malformed URL in proxy.ts links to a doc page that doesn't exist referencing "middleware" instead](https://github.com/vercel/next.js/issues/86190)**
   - **User:** mohammed5920
   - **Created At:** 2025-11-16
   - **Summary:** The documentation link for a proxy-related error is outdated and leads to a 404 page. The user notes that the term "middleware" was not updated to "proxy" in the error message.

3. **[hydration bug](https://github.com/vercel/next.js/issues/86184)**
   - **User:** AlexeyLoktev
   - **Created At:** 2025-11-16
   - **Labels:** Turbopack, Error Handling, React
   - **Summary:** This issue describes a hydration error that occurs when refreshing the page after making changes to a component. The server executes an outdated version of the source code, leading to mismatched content.

4. **[Navigation to routes is blocked/delayed until prefetch requests complete in Next.js 16 with CacheComponents](https://github.com/vercel/next.js/issues/86182)**
   - **User:** arfa123
   - **Created At:** 2025-11-16
   - **Labels:** Linking and Navigating, Loading UI and Streaming
   - **Summary:** The issue highlights that navigation is delayed until prefetch requests complete, resulting in a poor user experience. This was identified after upgrading to Next.js 16.

5. **[Turbopack passes `params` as a Promise instead of an object in dynamic App Router routes](https://github.com/vercel/next.js/issues/86173)**
   - **User:** willardcsoriano
   - **Created At:** 2025-11-16
   - **Labels:** Turbopack
   - **Summary:** This issue reports that Turbopack incorrectly passes route parameters as a Promise, causing errors in dynamic routes. The problem does not occur in production builds.

## Categorization of Issues

- **Documentation Issues:**
  - Issue 2 (Malformed URL in documentation)

- **Functional Bugs:**
  - Issue 1 (Infinite Loop)
  - Issue 3 (Hydration Bug)
  - Issue 4 (Navigation Delay)
  - Issue 5 (Turbopack Parameter Issue)

## Analysis and Recommendations

### Key Themes:
- **Documentation Gaps:** There is a clear need for updates in the documentation to reflect recent changes in the framework, particularly regarding the transition from "middleware" to "proxy."
- **Hydration and Navigation Issues:** Multiple issues are related to hydration errors and navigation delays, which can significantly impact user experience.

### Recommendation:
The **[not-found.tsx: Infinite Loop when a Component Calls router.refresh](https://github.com/vercel/next.js/issues/86197)** issue should be prioritized. This issue not only affects the functionality of the application but also leads to a poor user experience due to infinite loops. Addressing this could prevent further complications in user navigation and application stability.

By focusing on this issue, the team can enhance the overall reliability of the Next.js framework and improve user satisfaction.