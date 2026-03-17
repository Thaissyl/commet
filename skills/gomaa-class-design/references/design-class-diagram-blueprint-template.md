# Design Class Diagram Blueprint Template

```markdown
# Design Class Diagram Blueprint: <System or Subsystem Name>

## Scope

- Included classes: `<ClassA>`, `<ClassB>`, `<ClassC>`
- Source artifacts: `<step-2.1>`, `<step-1.3 files>`, `<step-2.2 files>`, `<optional step-2.3 files>`

## Class Boxes

### `<ClassName>`

- Stereotype: `<<...>>`
- Attributes:
  - `- <attributeName>: <type>`
  - `- <attributeName>: <type>`
- Operations:
  - `+ <operationName>(in <inputParam>, out <outputParam>)`
  - `+ <operationName>(in <inputParam>, out <outputParam>)`

### `<ClassName>`

- Stereotype: `<<...>>`
- Attributes:
  - `- <attributeName>: <type>`
- Operations:
  - `+ <operationName>(in <inputParam>, out <outputParam>)`
  - `none in current scope` if the class is purely structural in the chosen scope

## Relationships

- `<ClassA>` `1` -- `0..*` `<ClassB>` : <association meaning>
- `<ClassC>` *-- `<ClassD>` : <composition meaning>
- `<Subclass>` --|> `<Superclass>`

## Notes

- Keep all attributes private.
- List only public operations that are justified by the dynamic model.
- For purely structural classes, list `none in current scope` instead of inventing operations.
- Preserve analysis relationships unless design evidence justifies a refinement.
```
