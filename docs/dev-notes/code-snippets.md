<!--
START OF: code-snippets.md
Purpose: A repository of useful, reusable code snippets that come handy during development.
Update Frequency: Add snippets as new common patterns or utilities emerge.
Location: docs/dev-notes/code-snippets.md
-->

# Code Snippets

---

## Snippet [#1] - [Descriptive function comment]

**Date:** <2025-06-26 Thu>
**Author:** Zubair

Description:
This snippet should be used with each and every function to avoid any confusion later.

### Python

```python
def function_name(param1: Type, param2: Type, optional_param: Type = default) -> ReturnType:
    """
    Brief description of what the function does.

    Parameters:
    - param1 (Type): Description. Include valid bounds, expected format, or units.
    - param2 (Type): Description. Note any constraints or relationships with other params.
    - optional_param (Type): What it does. Default is X. Mention when/why it should be changed.

    Returns:
    - ReturnType: Description of what is returned, structure, and any edge cases.

    Raises:
    - SpecificError: When this condition happens.
    - AnotherError: When something else goes wrong.

    """
    pass  # your implementation here

```

### Javascript

```js
/**
 * short function description
 *
 * @param {type} param1 - description
 * @param {type} param2 - description
 * @param {type} [param3=default_value] - description. what to do, when.
 *
 * @returns {type} - description
 *
 * @throws {Error} - description
 * @throws {Error} - description
 *
 * @example
 * type result = func(arg, 'arg');
 */
function func(param1, param2, param=default_value) {
   // implementation
}
```

#### Pro Tips:

- Keep parameter constraints near the top.
- Mention side effects like DB access, file I/O, or external API calls.
- Always show a usage example in the docstring.
- If returning a dictionary, specify expected keys.
- Don’t forget to document exceptions, especially in critical systems.

---

## Snippet [#2] -

---

## Notes

* Keep snippets small and focused.
* Reference source or inspiration, if applicable.

<!-- END OF code-snippets.md -->
