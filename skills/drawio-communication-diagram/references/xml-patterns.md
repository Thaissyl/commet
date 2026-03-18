# XML Patterns

Use `mcp__drawio__open_drawio_xml` as the primary rendering path.
Use draw.io XML for the final artifact because communication diagrams in this style need draw.io actor shapes, plain associations, and grouped directional message blocks.

## Base Document

Start from a normal draw.io XML skeleton:

```xml
<mxfile host="app.diagrams.net">
  <diagram name="UC-Example">
    <mxGraphModel grid="1" gridSize="10" page="1" pageScale="1" pageWidth="1100" pageHeight="850">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Keep coordinates on a 10 px grid.
Use enough whitespace around associations to hold grouped message blocks.

## Software Object Recipe

Use a standard rectangle vertex for each software object.

- Shape: rectangle
- Fill: `#82CAFA`
- Stroke: black
- Text: centered, two lines
- Top line: rendered stereotype with guillemets, for example `&#171;coordinator&#187;`
- Bottom line: `: SearchCoordinator`

Recommended style:

```text
rounded=0;whiteSpace=wrap;html=1;fillColor=#82CAFA;strokeColor=#000000;align=center;verticalAlign=middle;fontColor=#000000;
```

Recommended size:

- width: 150-190
- height: 60-80

## Actor Recipe

Use the built-in draw.io UML actor shape.

- Shape: UML actor
- Fill: `#82CAFA`
- Stroke: black
- Label: actor name, shown with the actor shape and no leading colon

Recommended style:

```text
shape=umlActor;whiteSpace=wrap;html=1;fillColor=#82CAFA;strokeColor=#000000;verticalLabelPosition=bottom;verticalAlign=top;align=center;
```

Recommended size:

- width: `40-60`
- height: `70-100`

## Association Recipe

Use a plain black edge for each structural link.

- no arrowheads
- thin black stroke
- orthogonal routing when it improves clarity

Recommended style:

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;startArrow=none;strokeColor=#000000;
```

These are structural links only.
Do not encode message direction on the association itself.

## Directional Group Recipe

Use one floating rounded rectangle vertex per exact message direction near the related association.

- group by exact source and target pair, for example `Visitor -> VisitorUI`
- keep the reverse direction in a separate block, for example `VisitorUI -> Visitor`
- block heading format: `A -> B`
- block body format: one line per message, for example `1.2: request initial published listings`
- do not repeat participant names inside the block body
- preserve message numbering exactly

Recommended style:

```text
rounded=1;whiteSpace=wrap;html=1;fillColor=#f8faff;strokeColor=#6c8ebf;dashed=1;arcSize=8;align=left;verticalAlign=top;spacing=10;fontColor=#000000;
```

Recommended sizing:

- width: 280-430
- height: fit content with 10 px inner padding

Legacy per-message text boxes and free-floating arrow connectors should be used only when the user explicitly asks for that more detailed style.

## Layout Heuristics

Use these defaults unless the source text clearly says otherwise:

- place the primary actor on the far left or bottom-left
- place the main coordinator or central object near the center
- place external-system actors and their proxies on the far right or bottom-right
- use horizontal spacing around `180-220`
- use vertical branch spacing around `120-160`
- keep at least `50-70` px of free space near a pathway that carries grouped message blocks
- stack opposite-direction group blocks near the same association when both directions are used
- keep block headings short and move long message content into the body lines

When the source includes an ASCII `Object Layout`, preserve its relative topology and branch direction, then adjust spacing locally to avoid collisions.

## Update Strategy

When editing an existing `.drawio`:

- preserve current coordinates and IDs when the existing structure is still valid
- patch local directional group blocks when the topology is unchanged
- rebuild the whole XML when topology, actor shape choice, or grouped-message placement must change substantially

## Minimal XML Example

Use this as a pattern, not as a fixed template:

```xml
<mxCell id="obj-search" value="&#171;coordinator&#187;&lt;br/&gt;: SearchCoordinator" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#82CAFA;strokeColor=#000000;align=center;verticalAlign=middle;fontColor=#000000;" vertex="1" parent="1">
  <mxGeometry x="360" y="180" width="170" height="70" as="geometry"/>
</mxCell>

<mxCell id="group-ui-to-search" value="&lt;b&gt;VisitorUI -&gt; SearchCoordinator&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;1.1: request search page&lt;br/&gt;2.1: submit criteria" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8faff;strokeColor=#6c8ebf;dashed=1;arcSize=8;align=left;verticalAlign=top;spacing=10;fontColor=#000000;" vertex="1" parent="1">
  <mxGeometry x="210" y="90" width="250" height="90" as="geometry"/>
</mxCell>
```
