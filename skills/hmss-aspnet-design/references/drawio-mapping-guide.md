# Draw.io Mapping Guide — HMSS ASP.NET Phase 3

How to turn step-3.0 and step-3.2 markdown files into draw.io XML for the HMSS ASP.NET simple layered backend pattern.

---

## Which Skill Renders Which File

| Source file | Invoked skill | Output file |
|---|---|---|
| `step-3.0-design-communication-diagram.md` | `drawio-communication-diagram` | `step-3.0-design-communication-diagram.drawio` |
| `step-3.2-design-class-diagram-blueprint.md` | `drawio-design-class-diagram` | `step-3.2-design-class-diagram-blueprint.drawio` |

---

## Step-3.0 → Communication Diagram

### Input sections consumed

| step-3.0 section | Drawio use |
|---|---|
| `Object Layout` (ASCII) | Determines participant placement topology |
| `Participants` table | Names, kinds (actor vs software object), stereotypes |
| `Messages` table | One floating text label + one short directional connector per message |

### Which objects belong as participants

Only include an object as a participant (box + association) if another object **sends a message to it** (calls one of its operations) within this UC.

- A class that appears only as a **data value in `out` parameters** (e.g. `out listings: RoomListingList`) is a data type being passed around — do NOT show it as a participant box or draw an association to it in the communication diagram.
- A `<<data abstraction>>` IS a participant when its operations are explicitly called (e.g. Controller → UserAccount: `applyStatusChange()`).
- A `<<data abstraction>>` is NOT a participant when it is only returned from a repository call and passed as a value to other methods without any direct method call on it.

The `<<data abstraction>>` class always belongs in the **class diagram (step-3.2)** regardless. The distinction is only about its presence in the **communication diagram (step-3.0)**.

### Participant → drawio element mapping

| Participant type | Drawio element | Shape style |
|---|---|---|
| Actor (primary / secondary) | UML actor shape | `shape=umlActor;fillColor=#82CAFA;strokeColor=#000000;verticalLabelPosition=bottom;` |
| `<<user interaction>>` | Software object box | fill `#dbeafe`, border `#93c5fd` |
| `<<coordinator>>` | Software object box | fill `#ffedd5`, border `#fdba74` |
| `<<database wrapper>>` | Software object box | fill `#dff6fb`, border `#7dd3c7` |
| `<<data abstraction>>` | Software object box | fill `#dff6fb`, border `#7dd3c7` |
| `<<service>>` | Software object box | fill `#ede9fe`, border `#c4b5fd` |
| `<<proxy>>` | Software object box | fill `#fce7f3`, border `#f9a8d4` |

Software object box text: two lines — stereotype on top, `: ClassName` on bottom.

```text
rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;align=center;verticalAlign=middle;fontColor=#000000;
```

### Message → drawio element mapping

Each message row `| # | From -> To | message |` becomes two drawio cells:
- **Text label**: floating vertex with the full message string (number + method signature)
- **Direction arrow**: short free-floating connector (no endpoint attachment), pointing from→to participant

Use `endArrow=classic;startArrow=none;strokeColor=#000000;` for the connector.
Do NOT attach the arrow to participant nodes — keep it free-floating near the association.

### HMSS layout rule for ASP.NET layered pattern

```
[Primary Actor] ─── [UI <<user interaction>>] ─── [Controller <<coordinator>>]
                                                         │
                                            ┌────────────┼────────────────────┐
                                            │            │                    │
                                    [IRepo <<db wrap>>]  [Service <<service>>]  [IGateway <<proxy>>] ─── [Ext Actor]
                                            │
                                    [Entity <<data abs>>]
```

- Primary actor: far left
- UI box: second from left
- Controller box: center (the hub)
- Repository: right of controller, slightly below
- Domain object: below/right of repository
- Service: below controller
- Gateway + External actor: far right
- Keep vertical spacing ≥ 140px between branch rows

---

## Step-3.2 → Design Class Diagram

### Input sections consumed

| step-3.2 section | Drawio use |
|---|---|
| `Class Boxes` → per-class subsections | Each becomes one three-row UML class cell |
| `Relationships` | Association/aggregation edges with navigability arrows |
| `Generalizations` | Inheritance edges (open triangle to superclass) |
| step-3.0 (cross-reference) | Layout order follows step-3.0 left-to-right participant flow |

### Class box → drawio element mapping

Each `### ClassName` block becomes one draw.io cell using an HTML table label:

```html
<table border="1" cellspacing="0" cellpadding="6" style="width:100%;height:100%;border-collapse:collapse;font-size:12px;border-color:{border};">
  <tr><td align="center" bgcolor="{header}"><font color="{accent}"><b>«{stereotype}»<br/>ClassName</b></font></td></tr>
  <tr><td align="left" bgcolor="{body}">- attr: Type<br/>- attr2: Type</td></tr>
  <tr><td align="left" bgcolor="{body}">+ method(in p: T, out r: R)<br/>+ asyncMethod(in p: T)</td></tr>
</table>
```

### Stereotype → color palette

| Stereotype | header bg | body bg | accent text | border |
|---|---|---|---|---|
| `user interaction` | `#dbeafe` | `#f8fbff` | `#1d4ed8` | `#93c5fd` |
| `coordinator` | `#ffedd5` | `#fff7ed` | `#c2410c` | `#fdba74` |
| `database wrapper` | `#dff6fb` | `#f7fcfd` | `#0f766e` | `#7dd3c7` |
| `data abstraction` | `#dff6fb` | `#f7fcfd` | `#0f766e` | `#7dd3c7` |
| `service` | `#ede9fe` | `#faf8ff` | `#7c3aed` | `#c4b5fd` |
| `proxy` | `#fce7f3` | `#fff7fb` | `#be185d` | `#f9a8d4` |

### Relationship → drawio edge mapping

All relationships in HMSS phase-3 ASP.NET use directed association (navigable from controller outward):

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;
strokeColor=#64748b;strokeWidth=1.4;endArrow=open;endFill=0;endSize=10;
```

Add multiplicity label vertices near each endpoint.
Add association name label vertex at mid-edge for named relationships.

### HMSS layout rule for class diagram

Follow the same left-to-right flow as step-3.0:

```
[UI]  →  [Controller]  →  [IRepository]
                │               ↓
                │         [DomainObject]
                │
                ├→  [Service]
                └→  [IGateway]
```

- UI class: leftmost column
- Controller: second column (hub)
- IRepository + DomainObject: third column (stacked vertically)
- Service and IGateway: fourth column (branching down from controller)
- Recommended horizontal spacing: 240–280px
- Recommended vertical spacing: 150–180px

---

## Invocation Sequence

1. Save `step-3.0-design-communication-diagram.md`
2. Immediately invoke `drawio-communication-diagram` skill with the saved file path → produces `step-3.0-design-communication-diagram.drawio`
3. Save `step-3.2-design-class-diagram-blueprint.md`
4. Immediately invoke `drawio-design-class-diagram` skill with the saved file path (also pass step-3.0 path for layout alignment) → produces `step-3.2-design-class-diagram-blueprint.drawio`
