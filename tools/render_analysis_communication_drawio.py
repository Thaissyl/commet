from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape


ACTOR_STYLE = (
    "shape=umlActor;whiteSpace=wrap;html=1;fillColor=#82CAFA;strokeColor=#000000;"
    "verticalLabelPosition=bottom;verticalAlign=top;align=center;"
)
OBJECT_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#82CAFA;strokeColor=#000000;"
    "align=center;verticalAlign=middle;fontColor=#000000;"
)
ASSOC_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "html=1;endArrow=none;startArrow=none;strokeColor=#000000;"
)
TEXT_STYLE = (
    "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;"
    "whiteSpace=wrap;fontColor=#000000;"
)
ARROW_STYLE = "edgeStyle=none;rounded=0;html=1;endArrow=classic;startArrow=none;strokeColor=#000000;"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text.replace("\n", "\r\n"), encoding="utf-8")


def find_heading(text: str, prefix: str) -> str | None:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line.strip()
    return None


def section_between(text: str, start_heading: str, stop_prefixes: list[str]) -> str:
    if start_heading not in text:
        return ""
    section = text.split(start_heading, 1)[1]
    lines = []
    for line in section.splitlines():
        if any(line.startswith(prefix) for prefix in stop_prefixes):
            break
        lines.append(line)
    return "\n".join(lines)


def parse_table(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if not parts or parts[0] in {"Position", "#"} or re.fullmatch(r"-+", parts[0] or ""):
            continue
        rows.append(parts)
    return rows


def parse_participants(text: str):
    start = find_heading(text, "## Participants")
    if not start:
        return []
    section = section_between(text, start, ["## Messages", "## Alternative", "## Architectural Notes"])
    participants = []
    for row in parse_table(section):
        name = row[1]
        stereotype = row[2]
        if "Actor" in stereotype:
            kind = "actor"
            role = "primary" if "primary" in stereotype.lower() else "secondary"
            stereo = None
        else:
            kind = "software_object"
            role = None
            stereo = stereotype.strip("`")
        participants.append({"name": name, "kind": kind, "role": role, "stereotype": stereo})
    return participants


def parse_messages(text: str):
    messages = []
    headings = []
    for prefix in ["## Messages", "## Alternative"]:
        heading = find_heading(text, prefix)
        if heading:
            headings.append(heading)
    for heading in headings:
        stop_prefixes = ["## Architectural Notes", "## Notes"]
        if heading.startswith("## Messages"):
            stop_prefixes.append("## Alternative")
        else:
            stop_prefixes.append("## ")
        section = section_between(text, heading, stop_prefixes)
        for row in parse_table(section):
            source_target = row[1]
            if "->" not in source_target:
                continue
            source, target = [part.strip() for part in source_target.split("->", 1)]
            messages.append({"number": row[0], "from": source, "to": target, "text": row[2]})
    return messages


def parse_object_layout_rows(text: str, participant_names: list[str]):
    start = find_heading(text, "## Object Layout")
    if not start:
        return []
    section = section_between(text, start, ["## Participants", "## Messages", "## Alternative", "## Architectural Notes"])
    fence_match = re.search(r"```(?:text)?\n(.*?)\n```", section, flags=re.DOTALL)
    if not fence_match:
        return []
    rows = []
    for row_idx, line in enumerate(fence_match.group(1).splitlines()):
        placements = []
        for name in sorted(participant_names, key=len, reverse=True):
            for match in re.finditer(re.escape(name), line):
                start_col = match.start()
                end_col = match.end()
                overlaps = any(not (end_col <= existing["start"] or start_col >= existing["end"]) for existing in placements)
                if not overlaps:
                    placements.append({"name": name, "start": start_col, "end": end_col})
        if placements:
            rows.append({"row": row_idx, "items": sorted(placements, key=lambda item: item["start"])})
    return rows


def message_sort_key(number: str):
    parts = re.findall(r"\d+|[A-Za-z]+", number)
    key = []
    for part in parts:
        key.append((0, int(part)) if part.isdigit() else (1, part))
    return key


def participant_id(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "participant"


def classify_groups(participants):
    primary_actors = [p for p in participants if p["kind"] == "actor" and p["role"] == "primary"]
    secondary_actors = [p for p in participants if p["kind"] == "actor" and p["role"] == "secondary"]
    ui = [p for p in participants if p["stereotype"] == "<<user interaction>>"]
    coordinator = [p for p in participants if p["stereotype"] == "<<coordinator>>"]
    business_logic = [p for p in participants if p["stereotype"] == "<<business logic>>"]
    proxies = [p for p in participants if p["stereotype"] == "<<proxy>>"]
    entities = [p for p in participants if p["stereotype"] == "<<entity>>"]
    others = [
        p
        for p in participants
        if p not in primary_actors + secondary_actors + ui + coordinator + business_logic + proxies + entities
    ]
    return primary_actors, secondary_actors, ui, coordinator, business_logic, proxies, entities, others


def preferred_box(participant):
    if participant["kind"] == "actor":
        return 50, 90
    width = max(170, min(220, 110 + len(participant["name"]) * 5))
    return width, 70


def layout_positions_from_object_layout(participants, text: str):
    rows = parse_object_layout_rows(text, [p["name"] for p in participants])
    if not rows:
        return None
    positions = {}
    for row in rows:
        y = 180 + row["row"] * 160
        for item in row["items"]:
            participant = next(p for p in participants if p["name"] == item["name"])
            width, height = preferred_box(participant)
            x = 40 + item["start"] * 8
            positions[participant["name"]] = {"x": x, "y": y, "w": width, "h": height}
    if len(positions) != len(participants):
        return None

    for y in sorted({pos["y"] for pos in positions.values()}):
        row_items = sorted(((name, pos) for name, pos in positions.items() if pos["y"] == y), key=lambda item: item[1]["x"])
        cursor = 40
        for _, pos in row_items:
            pos["x"] = max(pos["x"], cursor)
            cursor = pos["x"] + pos["w"] + 80

    return positions


def fallback_layout_positions(participants):
    primary_actors, secondary_actors, ui, coordinator, business_logic, proxies, entities, others = classify_groups(participants)
    positions = {}

    def place(items, x: int, start_y: int, step_y: int, width: int, height: int):
        for idx, p in enumerate(items):
            positions[p["name"]] = {"x": x, "y": start_y + idx * step_y, "w": width, "h": height}

    place(primary_actors, 40, 420, 120, 50, 90)
    place(ui, 180, 430, 120, 180, 70)
    place(coordinator, 460, 430, 120, 200, 70)
    place(business_logic, 760, 210, 140, 180, 70)
    place(entities, 1040, 190, 140, 180, 70)
    place(proxies, 760, 650, 140, 190, 70)
    place(secondary_actors, 1050, 640, 140, 50, 90)
    place(others, 1040, 430, 140, 180, 70)
    return positions


def layout_positions(participants, text: str):
    return layout_positions_from_object_layout(participants, text) or fallback_layout_positions(participants)


def center(box):
    return box["x"] + box["w"] / 2, box["y"] + box["h"] / 2


def association_pairs(messages):
    pairs = []
    seen = set()
    for msg in messages:
        pair = tuple(sorted((msg["from"], msg["to"])))
        if pair in seen:
            continue
        seen.add(pair)
        pairs.append(pair)
    return pairs


def grouped_messages(messages):
    grouped = {}
    for msg in sorted(messages, key=lambda item: message_sort_key(item["number"])):
        pair = tuple(sorted((msg["from"], msg["to"])))
        grouped.setdefault(pair, []).append(msg)
    return grouped


def text_box_size(text: str):
    width = min(420, max(150, 8 * len(text) + 30))
    height = 24 if len(text) < 42 else 38 if len(text) < 85 else 52
    return width, height


def render(source: Path, output: Path):
    text = read(source)
    participants = parse_participants(text)
    messages = parse_messages(text)
    if not participants or not messages:
        raise ValueError(f"Could not parse participants/messages from {source}")
    names = {p["name"] for p in participants}
    unknown = sorted({m["from"] for m in messages if m["from"] not in names} | {m["to"] for m in messages if m["to"] not in names})
    if unknown:
        raise ValueError(f"Unknown endpoints in {source.name}: {', '.join(unknown)}")

    positions = layout_positions(participants, text)
    pair_messages = grouped_messages(messages)
    page_height = max(1200, 980 + max(0, len(messages) - 18) * 18)

    xml = [
        '<mxfile host="app.diagrams.net">',
        f'  <diagram id="{escape(source.stem)}" name="{escape(source.stem)}">',
        f'    <mxGraphModel dx="1600" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="{page_height}" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>',
    ]

    for p in participants:
        pid = participant_id(p["name"])
        pos = positions[p["name"]]
        if p["kind"] == "actor":
            value = escape(p["name"])
            style = ACTOR_STYLE
        else:
            stereo = p["stereotype"].strip("`")
            value = f"&#171;{escape(stereo.strip('<>'))}&#187;&lt;br/&gt;: {escape(p['name'])}"
            style = OBJECT_STYLE
        xml.append(
            f'        <mxCell id="{pid}" value="{value}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{int(pos["x"])}" y="{int(pos["y"])}" width="{int(pos["w"])}" height="{int(pos["h"])}" as="geometry"/></mxCell>'
        )

    for idx, (a, b) in enumerate(association_pairs(messages), 1):
        xml.append(
            f'        <mxCell id="assoc-{idx}" style="{ASSOC_STYLE}" edge="1" parent="1" source="{participant_id(a)}" target="{participant_id(b)}">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    for pair_idx, ((a, b), items) in enumerate(pair_messages.items(), 1):
        box_a = positions[a]
        box_b = positions[b]
        ax, ay = center(box_a)
        bx, by = center(box_b)
        dx = bx - ax
        dy = by - ay
        length = math.hypot(dx, dy) or 1.0
        ux = dx / length
        uy = dy / length
        px = -uy
        py = ux
        mid_x = (ax + bx) / 2
        mid_y = (ay + by) / 2
        for msg_idx, msg in enumerate(items):
            label = f"{msg['number']}: {msg['text']}"
            width, height = text_box_size(label)
            offset = (msg_idx - (len(items) - 1) / 2) * 34
            text_x = mid_x + px * offset - width / 2
            text_y = mid_y + py * offset - height / 2 - 18
            xml.append(
                f'        <mxCell id="msg-{pair_idx}-{msg_idx}" value="{escape(label)}" style="{TEXT_STYLE}" vertex="1" parent="1">'
                f'<mxGeometry x="{int(text_x)}" y="{int(text_y)}" width="{int(width)}" height="{int(height)}" as="geometry"/></mxCell>'
            )
            forward = 1 if (msg["from"] == a and msg["to"] == b) else -1
            start_x = text_x + width / 2 - 20 * forward * ux
            start_y = text_y + height + 6
            end_x = start_x + forward * 55 * ux
            end_y = start_y + forward * 55 * uy
            xml.append(
                f'        <mxCell id="msg-{pair_idx}-{msg_idx}-arrow" style="{ARROW_STYLE}" edge="1" parent="1">'
                f'<mxGeometry relative="1" as="geometry"><mxPoint x="{int(start_x)}" y="{int(start_y)}" as="sourcePoint"/>'
                f'<mxPoint x="{int(end_x)}" y="{int(end_y)}" as="targetPoint"/></mxGeometry></mxCell>'
            )

    note = (
        f"Regenerated from {source.name}. Positions prefer the explicit Object Layout when available, while associations still follow direct message pathways if the layout and message table diverge."
    )
    xml.append(
        '        <mxCell id="note-1" value="'
        + escape(note)
        + '" style="shape=note;whiteSpace=wrap;html=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;align=left;verticalAlign=top;spacingTop=6;spacingLeft=8;" vertex="1" parent="1"><mxGeometry x="40" y="980" width="760" height="90" as="geometry"/></mxCell>'
    )
    xml += ["      </root>", "    </mxGraphModel>", "  </diagram>", "</mxfile>"]
    write(output, "\n".join(xml))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: render_analysis_communication_drawio.py <source.md> <output.drawio>")
    render(Path(sys.argv[1]), Path(sys.argv[2]))
