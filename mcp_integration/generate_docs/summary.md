# Summary for vercel/next.js



---

# Directory Structure of the Vercel Next.js Repository

```
- [.alexignore](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.alexignore)
- [.alexrc](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.alexrc)
- [.cargo](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.cargo)
- [.config](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.config)
- [.cursorindexingignore](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.cursorindexingignore)
- [.devcontainer](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.devcontainer)
- [.git-blame-ignore-revs](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.git-blame-ignore-revs)
- [.gitattributes](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.gitattributes)
- [.github](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.github)
- [.husky](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.husky)
- [.ignore](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.ignore)
- [.node-version](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.node-version)
- [.npmrc](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.npmrc)
- [.prettierignore](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.prettierignore)
- [.prettierrc.json](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.prettierrc.json)
- [.rustfmt.toml](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.rustfmt.toml)
- [.typos.toml](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.typos.toml)
- [.vscode](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/.vscode)
- [CODE_OF_CONDUCT.md](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/CODE_OF_CONDUCT.md)
- [Cargo.lock](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/Cargo.lock)
- [Cargo.toml](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/Cargo.toml)
- [UPGRADING.md](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/UPGRADING.md)
- [apps](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/apps)
- [bench](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/bench)
- [contributing.md](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/contributing.md)
- [contributing](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/contributing)
- [crates](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/crates)
- [docs](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/docs)
- [errors](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/errors)
- [eslint.cli.config.mjs](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/eslint.cli.config.mjs)
- [eslint.config.mjs](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/eslint.config.mjs)
- [examples](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/examples)
- [jest.config.js](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/jest.config.js)
- [jest.config.turbopack.js](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/jest.config.turbopack.js)
- [lerna.json](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/lerna.json)
- [license.md](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/license.md)
- [lint-staged.config.js](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/lint-staged.config.js)
- [package.json](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/package.json)
- [packages](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/packages)
- [patches](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/patches)
- [pnpm-lock.yaml](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/pnpm-lock.yaml)
- [pnpm-workspace.yaml](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/pnpm-workspace.yaml)
- [readme.md](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/readme.md)
- [release.js](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/release.js)
- [rspack](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/rspack)
- [run-tests.js](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/run-tests.js)
- [rust-toolchain.toml](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/rust-toolchain.toml)
- [scripts](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/scripts)
- [sgconfig.yml](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/sgconfig.yml)
- [socket.yaml](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/socket.yaml)
- [test-config-errors](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/test-config-errors)
- [test-file.txt](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/test-file.txt)
- [test](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/test)
- [tsconfig-tsec.json](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/tsconfig-tsec.json)
- [tsconfig.json](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/tsconfig.json)
- [tsec-exemptions.json](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/tsec-exemptions.json)
- [turbo.json](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/turbo.json)
- [turbo](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/turbo)
- [turbopack](https://github.com/vercel/next.js/tree/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/turbopack)
- [vercel.json](https://github.com/vercel/next.js/blob/a3aadbd37c2c19bdeac021b78a474d90bff9f9c0/vercel.json)
```

---

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

---

# Summary of Recent Pull Requests for Vercel/Next.js

## 1. [Update Rspack production test manifest](https://github.com/vercel/next.js/pull/86200)
- **Created At:** 2025-11-17
- **User:** [vercel-release-bot](https://github.com/vercel-release-bot)
- **Labels:** tests, run-react-18-tests
- **Summary:** This PR updates the production integration test manifest used when testing Rspack.

## 2. [Update Rspack development test manifest](https://github.com/vercel/next.js/pull/86201)
- **Created At:** 2025-11-17
- **User:** [vercel-release-bot](https://github.com/vercel-release-bot)
- **Labels:** tests, run-react-18-tests
- **Summary:** This PR updates the development integration test manifest used when testing Rspack.

## 3. [Model `||`, `&&`, and `??` as control flow operators](https://github.com/vercel/next.js/pull/85837)
- **Created At:** 2025-11-05
- **User:** [lukesandberg](https://github.com/lukesandberg)
- **Labels:** Font (next/font), Turbopack, created-by: Turbopack team, tests
- **Summary:** This PR handles control flow operators in the turbopack analyzer to trigger dead code handling and trim dependencies from dead branches.

## 4. [Feature/410 Gone Status Feature](https://github.com/vercel/next.js/pull/78706)
- **Created At:** 2025-04-30
- **User:** [Sam7](https://github.com/Sam7)
- **Labels:** examples, type: next, Documentation, tests, Rspack
- **Summary:** This PR adds support for HTTP 410 Gone status in Next.js, providing developers with a way to indicate that content has been permanently removed.

## 5. [Update 14-metadata-and-og-images.mdx](https://github.com/vercel/next.js/pull/86198)
- **Created At:** 2025-11-17
- **User:** [jokokoloko](https://github.com/jokokoloko)
- **Labels:** Documentation
- **Summary:** This PR changes example images to better match and be consistent within documentation copy.

---

### Key Themes:
- **Testing Enhancements:** The recent pull requests focus on updating test manifests for Rspack, indicating ongoing improvements in testing practices.
- **Control Flow Operators:** The handling of control flow operators in Turbopack suggests a focus on optimizing the build process and improving performance.
- **New Features:** The introduction of the 410 Gone status feature highlights a commitment to enhancing the framework's capabilities and improving SEO and user experience.

### Recommendations:
- **Prioritize Testing Updates:** Ensure that the updates to the Rspack test manifests are thoroughly reviewed and integrated to maintain testing integrity.
- **Monitor Control Flow Changes:** Keep an eye on the implementation of control flow operators to assess their impact on performance and functionality.
- **Documentation Consistency:** Ensure that documentation is updated in line with new features to provide clear guidance to developers.

---

# Summary of Branches in Vercel/Next.js Repository

## Branches

1. **Branch Name:** [01-02-Copy_58398](https://api.github.com/repos/vercel/next.js/commits/4fbe6778e0ce5562235f21d8540374e1680daf7c)
   - **Commit SHA:** 4fbe6778e0ce5562235f21d8540374e1680daf7c
   - **Protected:** No

2. **Branch Name:** [01-02-Rename___next_f_to___rsc_payload](https://api.github.com/repos/vercel/next.js/commits/e1b2ad4f96a019d753eed60caa8bde94aad1b4ad)
   - **Commit SHA:** e1b2ad4f96a019d753eed60caa8bde94aad1b4ad
   - **Protected:** No

3. **Branch Name:** [01-02-Try_removing_partial_manifest](https://api.github.com/repos/vercel/next.js/commits/c9a7ecefaf86ebf0b199284a92c3b1423331846c)
   - **Commit SHA:** c9a7ecefaf86ebf0b199284a92c3b1423331846c
   - **Protected:** No

4. **Branch Name:** [01-03--_implemented_api_invocation_logic_for_feedback_thumb_up_down_-_added_component_test_to_erroroverlaylayout_and_fixed_bug_in_clip-rule_etc](https://api.github.com/repos/vercel/next.js/commits/fe6af7e97d18dcd76a0810257c9416502d058f59)
   - **Commit SHA:** fe6af7e97d18dcd76a0810257c9416502d058f59
   - **Protected:** No

5. **Branch Name:** [01-05-Rename_acceptance_directory_to_acceptance-pages](https://api.github.com/repos/vercel/next.js/commits/9e7ced7ab8703a2daa261c8d0af4e9c78ca9bd37)
   - **Commit SHA:** 9e7ced7ab8703a2daa261c8d0af4e9c78ca9bd37
   - **Protected:** No