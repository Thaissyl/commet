# XML Patterns

Use `mcp__drawio__open_drawio_xml` as the primary rendering path.
Use draw.io XML for the final artifact because this skill needs editable UML-style class boxes and relationship edges.

## Base Document

Start from a normal draw.io XML skeleton:

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Example Class Diagram">
    <mxGraphModel grid="1" gridSize="10" page="1" pageScale="1" pageWidth="1400" pageHeight="1000">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Keep coordinates on a 10 px grid.
Use enough whitespace around edges to hold multiplicity labels cleanly.

## Class Box Recipe

Render each class as one simple draw.io cell.
Do not build class boxes from nested swimlanes or child compartments.

Use a plain rectangle cell whose HTML label contains a three-row table:
- header row: stereotype and class name
- attributes row
- operations row

## Layer Color Palette

Apply a consistent visual palette by stereotype or layer.

- `user interaction`, `boundary`, `gui`
  - header background `#dbeafe`
  - body background `#f8fbff`
  - accent text `#1d4ed8`
  - border `#93c5fd`
- `coordinator`, `control`
  - header background `#ffedd5`
  - body background `#fff7ed`
  - accent text `#c2410c`
  - border `#fdba74`
- `business logic`, `application logic`
  - header background `#dcfce7`
  - body background `#f7fdf9`
  - accent text `#15803d`
  - border `#86efac`
- `data abstraction`, `database wrapper`, `entity`
  - header background `#dff6fb`
  - body background `#f7fcfd`
  - accent text `#0f766e`
  - border `#7dd3c7`
- `service`
  - header background `#ede9fe`
  - body background `#faf8ff`
  - accent text `#7c3aed`
  - border `#c4b5fd`
- `proxy`
  - header background `#fce7f3`
  - body background `#fff7fb`
  - accent text `#be185d`
  - border `#f9a8d4`

When a stereotype is unknown, fall back to:
- header background `#e5e7eb`
- body background `#ffffff`
- accent text `#334155`
- border `#94a3b8`

Recommended class cell style:

```text
shape=rect;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;overflow=fill;spacing=0;
```

Recommended label pattern:

```html
<table border="1" cellspacing="0" cellpadding="6" style="width:100%;height:100%;border-collapse:collapse;font-size:12px;border-color:#93c5fd;">
  <tr>
    <td align="center" bgcolor="#dbeafe">
      <font color="#1d4ed8"><b>&#171;stereotype&#187;<br/>ClassName</b></font>
    </td>
  </tr>
  <tr>
    <td align="left" bgcolor="#f8fbff">
      - attributeA: Type<br/>- attributeB: Type
    </td>
  </tr>
  <tr>
    <td align="left" bgcolor="#f8fbff">
      + operationA(...)<br/>+ operationB(...)
    </td>
  </tr>
</table>
```

Recommended sizing:
- class width: `260-360`
- class height: size to content, usually `100-260`
- keep classes on a clean row or column grid

## Relationship Edge Recipes

### Association

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#64748b;strokeWidth=1.4;endArrow=open;endFill=0;endSize=10;
```

### Aggregation

Put the diamond on the whole side.

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#64748b;strokeWidth=1.4;startArrow=diamond;startFill=0;endArrow=open;endFill=0;endSize=10;
```

### Composition

Put the filled diamond on the whole side.

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#64748b;strokeWidth=1.4;startArrow=diamond;startFill=1;endArrow=open;endFill=0;endSize=10;
```

### Generalization

Point the open triangle to the superclass.

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#64748b;strokeWidth=1.4;endArrow=block;endFill=0;startArrow=none;
```

## Multiplicity Label Recipe

Render multiplicities as separate small text vertices near each end of the relationship edge.
Do not merge both multiplicities into the edge label.

Recommended style:

```text
text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontColor=#475569;
```

Keep each multiplicity label close to its endpoint but not overlapping the class border or arrowhead.

## Relationship Label Recipe

Use a separate text vertex for the association name instead of placing long prose directly on the edge.

Recommended style:

```text
text;html=1;strokeColor=none;fillColor=#ffffff;align=center;verticalAlign=middle;whiteSpace=wrap;fontColor=#334155;fontStyle=1;
```

Rules:
- use `association_name` as the displayed label when it exists
- add a reading-direction marker to the label, for example `manages >`, `< reads`, `updates v`, or `^ inherits`
- if only long prose is available, reduce it to a short readable verb phrase when that reduction is obvious; otherwise omit the association-name label
- keep the label close to the visual midpoint of the dominant segment of the edge

## Navigability Recipe

Use arrowheads to show navigability.

- target only navigable: `endArrow=open;endFill=0;startArrow=none`
- source only navigable: `startArrow=open;startFill=0;endArrow=none`
- bidirectional navigable: `startArrow=open;startFill=0;endArrow=open;endFill=0`
- no navigability shown: `startArrow=none;endArrow=none`

When the association name already contains a reading-direction marker, keep the actual navigability arrowhead as the authoritative notation and treat the marker as a readability aid.

## Note Recipe

Render notes as separate note cells when the source includes a `Notes` section.

Recommended note style:

```text
shape=note;whiteSpace=wrap;html=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;align=left;verticalAlign=top;spacingTop=6;spacingLeft=8;
```

Placement rules:
- place class-local notes near the referenced class when the note begins with `ClassName:`
- place global notes in a note column below or to the right of the main diagram
- do not connect notes with extra edges unless the user explicitly wants annotated connectors

## Layout Heuristics

Use these defaults unless the blueprint or user says otherwise:

- boundary or user interaction classes to the left
- coordinators and business logic near the center
- data abstractions to the right or lower-right
- services and proxies below or to the right of the coordinating class
- superclasses above subclasses when generalization exists
- keep the main association chain on one row when possible
- keep a bottom or right-side strip free for optional notes only when notes are actually rendered
- avoid crossing the main horizontal association chain with service or proxy edges

Recommended spacing:
- horizontal spacing around `220-280`
- vertical spacing around `140-180`
- keep at least `80` px between parallel edges when possible

## Update Strategy

When editing an existing `.drawio`:

- preserve current coordinates and IDs when the class set and topology are still valid
- patch only changed labels, members, and multiplicities when the structure is unchanged
- rebuild the whole XML when the class set, generalization tree, or major layout changed substantially

## Minimal XML Example

Use this as a pattern, not as a fixed template:

```xml
<mxCell id="class-roomlisting" value="&lt;table border=&quot;1&quot; cellspacing=&quot;0&quot; cellpadding=&quot;6&quot; style=&quot;width:100%;height:100%;border-collapse:collapse;font-size:12px;&quot;&gt;&lt;tr&gt;&lt;td align=&quot;center&quot;&gt;&lt;b&gt;&#171;data abstraction&#187;&lt;br/&gt;RoomListing&lt;/b&gt;&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td align=&quot;left&quot;&gt;- title: Text&lt;br/&gt;- status: RoomListingStatus&lt;br/&gt;- visibility: ListingVisibility&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td align=&quot;left&quot;&gt;+ getListingDetail(in listingReference, out listingDetail)&lt;br/&gt;+ applyAdminDisable(in listingReference, in listingControlAction, out listingVisibilityRecord)&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;" style="shape=rect;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;overflow=fill;spacing=0;" vertex="1" parent="1">
  <mxGeometry x="760" y="220" width="300" height="180" as="geometry"/>
</mxCell>

<mxCell id="edge-roomlistinglogic-roomlisting" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#64748b;strokeWidth=1.4;endArrow=open;endFill=0;endSize=10;" edge="1" parent="1" source="class-roomlistinglogic" target="class-roomlisting">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<mxCell id="label-roomlistinglogic-roomlisting" value="updates &gt;" style="text;html=1;strokeColor=none;fillColor=#ffffff;align=center;verticalAlign=middle;whiteSpace=wrap;fontColor=#334155;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="650" y="300" width="90" height="24" as="geometry"/>
</mxCell>
```
